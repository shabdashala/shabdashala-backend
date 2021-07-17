from django.db import models

from django_extensions.db.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _


class Language(TimeStampedModel):
    name = models.CharField(max_length=50)
    english_name = models.CharField(max_length=50)
    two_letter_code = models.CharField(max_length=5)
    three_letter_code = models.CharField(max_length=5)
    display_order = models.PositiveIntegerField(_("Display order"))
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return "{} ({})".format(self.name, self.english_name)
