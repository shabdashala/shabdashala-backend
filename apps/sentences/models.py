import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django_extensions.db.models import TimeStampedModel

from apps.sentences import managers as sentences_managers


class Sentence(TimeStampedModel):
    """
    A Sentence in a language. Uses :py:mod:`django-treebeard`.
    """
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    language = models.ForeignKey('languages.Language', on_delete=models.CASCADE)
    categories = models.ManyToManyField('categories.Category', blank=True)
    translations = models.ManyToManyField('self', blank=True)
    text = models.TextField(_('text'), max_length=2048)
    is_active = models.BooleanField(default=False)

    is_deleted = models.BooleanField(_('Is Deleted?'), default=False, db_index=True)
    date_removed = models.DateTimeField(null=True, blank=True, db_index=True)

    objects = sentences_managers.SentenceManager()

    class Meta:
        verbose_name = _('Sentence')
        verbose_name_plural = _('Sentences')

    def __str__(self):
        return self.text

    def delete(self, **kwargs):
        self.is_deleted = True
        self.date_removed = timezone.now()
        self.save()
