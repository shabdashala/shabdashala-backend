from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django_extensions.db.models import TimeStampedModel

from . import managers as languages_managers


class Language(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)
    english_name = models.CharField(max_length=50, unique=True)
    two_letter_code = models.CharField(max_length=5, unique=True)
    three_letter_code = models.CharField(max_length=5, unique=True)
    display_order = models.PositiveIntegerField(_("Display order"), default=0)
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(_('Is Deleted?'), default=False, db_index=True)
    date_removed = models.DateTimeField(null=True, blank=True, db_index=True)
    objects = languages_managers.LanguageManager()

    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')

    def __str__(self):
        return "{} ({})".format(self.name, self.english_name)

    def delete(self, **kwargs):
        self.is_deleted = True
        self.date_removed = timezone.now()
        self.save()
