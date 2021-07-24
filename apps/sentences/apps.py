from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SentencesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.sentences'
    verbose_name = _('Sentences')

