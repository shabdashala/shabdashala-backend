import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from django_extensions.db.models import TimeStampedModel


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

    class Meta:
        verbose_name = _('Sentence')
        verbose_name_plural = _('Sentences')

    def __str__(self):
        return self.text
