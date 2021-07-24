from django.db import models

from django_extensions.db.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _


class Language(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)
    english_name = models.CharField(max_length=50, unique=True)
    two_letter_code = models.CharField(max_length=5, unique=True)
    three_letter_code = models.CharField(max_length=5, unique=True)
    display_order = models.PositiveIntegerField(_("Display order"), default=0)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')

    def __str__(self):
        return "{} ({})".format(self.name, self.english_name)
