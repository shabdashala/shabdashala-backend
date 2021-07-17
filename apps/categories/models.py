import uuid

from django.core.cache import cache
from django.db import models
from django.db.models import Exists, OuterRef
from django.template.defaultfilters import striptags
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

from django_extensions.db.fields import AutoSlugField

from treebeard.mp_tree import MP_Node

from . import managers as categories_managers


class Category(MP_Node):
    """
    A language word/sentence category. Uses :py:mod:`django-treebeard`.
    """
    COMPARISON_FIELDS = ('pk', 'path', 'depth')
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    language = models.ForeignKey('languages.Language', on_delete=models.CASCADE)
    name = models.CharField(_('Name'), max_length=255, db_index=True)
    description = models.TextField(_('Description'), blank=True)
    meta_title = models.CharField(_('Meta title'), max_length=255, blank=True, null=True)
    meta_description = models.TextField(_('Meta description'), blank=True, null=True)
    image = models.ImageField(_('Image'), upload_to='categories', blank=True,
                              null=True, max_length=255)
    slug = AutoSlugField(_('Slug'), populate_from='name', max_length=255, db_index=True)

    is_public = models.BooleanField(
        _('Is public'),
        default=True,
        db_index=True,
        help_text=_("Show this category in search results and categories listings."))

    ancestors_are_public = models.BooleanField(
        _('Ancestor categories are public'),
        default=True,
        db_index=True,
        help_text=_("The ancestors of this category are public"))
    display_order = models.PositiveIntegerField(_("Display order"))

    is_active = models.BooleanField(default=False)

    _slug_separator = '/'
    _full_name_separator = ' > '

    objects = categories_managers.CategoryQuerySet.as_manager()

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        """
        Returns a string representation of the category and it's ancestors,
        e.g. 'Books > Non-fiction > Essential programming'.
        """
        names = [category.name for category in self.get_ancestors_and_self()]
        return self._full_name_separator.join(names)

    def get_full_slug(self, parent_slug=None):
        if self.is_root():
            return self.slug

        cache_key = self.get_url_cache_key()
        full_slug = cache.get(cache_key)
        if full_slug is None:
            parent_slug = parent_slug if parent_slug is not None else self.get_parent().full_slug
            full_slug = "%s%s%s" % (parent_slug, self._slug_separator, self.slug)
            cache.set(cache_key, full_slug)

        return full_slug

    @property
    def full_slug(self):
        """
        Returns a string of this category's slug concatenated with the slugs
        of it's ancestors, e.g. 'books/non-fiction/essential-programming'.
        Oscar used to store this as in the 'slug' model field, but this field
        has been re-purposed to only store this category's slug and to not
        include it's ancestors' slugs.
        """
        return self.get_full_slug()

    def generate_slug(self):
        """
        Generates a slug for a category. This makes no attempt at generating
        a unique slug.
        """
        return slugify(self.name)

    def save(self, *args, **kwargs):
        """
        Oscar traditionally auto-generated slugs from names. As that is
        often convenient, we still do so if a slug is not supplied through
        other means. If you want to control slug creation, just create
        instances with a slug already set, or expose a field on the
        appropriate forms.
        """
        if not self.slug:
            self.slug = self.generate_slug()
        super().save(*args, **kwargs)

    def set_ancestors_are_public(self):
        # Update ancestors_are_public for the sub tree.
        # note: This doesn't trigger a new save for each instance, rather
        # just a SQL update.
        included_in_non_public_subtree = self.__class__.objects.filter(
            is_public=False, path__rstartswith=OuterRef("path"), depth__lt=OuterRef("depth")
        )
        self.get_descendants_and_self().update(
            ancestors_are_public=Exists(
                included_in_non_public_subtree.values("id"), negated=True))

        # Correctly populate ancestors_are_public
        self.refresh_from_db()

    @classmethod
    def fix_tree(cls, destructive=False, fix_paths=False):
        super().fix_tree(destructive, fix_paths)
        for node in cls.get_root_nodes():
            # ancestors_are_public *must* be True for root nodes, or all trees
            # will become non-public
            if not node.ancestors_are_public:
                node.ancestors_are_public = True
                node.save()
            else:
                node.set_ancestors_are_public()

    def get_meta_title(self):
        return self.meta_title or self.name

    def get_meta_description(self):
        return self.meta_description or striptags(self.description)

    def get_ancestors_and_self(self):
        """
        Gets ancestors and includes itself. Use treebeard's get_ancestors
        if you don't want to include the category itself. It's a separate
        function as it's commonly used in templates.
        """
        if self.is_root():
            return [self]

        return list(self.get_ancestors()) + [self]

    def get_descendants_and_self(self):
        """
        Gets descendants and includes itself. Use treebeard's get_descendants
        if you don't want to include the category itself. It's a separate
        function as it's commonly used in templates.
        """
        return self.get_tree(self)

    def get_url_cache_key(self):
        current_locale = get_language()
        cache_key = 'CATEGORY_URL_%s_%s' % (current_locale, self.pk)
        return cache_key

    def _get_absolute_url(self, parent_slug=None):
        """
        Our URL scheme means we have to look up the category's ancestors. As
        that is a bit more expensive, we cache the generated URL. That is
        safe even for a stale cache, as the default implementation of
        `WordCategoryView` or `SentenceCategoryView` does the lookup via primary key anyway.
        But if you change that logic, you'll have to reconsider the caching approach.
        """
        return reverse('categories:detail', kwargs={
            'slug': self.get_full_slug(parent_slug=parent_slug),
            'pk': self.pk
        })

    def get_absolute_url(self):
        return self._get_absolute_url()

    class Meta:
        app_label = 'categories'
        ordering = ['path']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def has_children(self):
        return self.get_num_children() > 0

    def get_num_children(self):
        return self.get_children().count()
