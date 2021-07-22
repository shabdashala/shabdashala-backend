from django.utils.translation import gettext as _

CONFIGURED = 'configured'
DYNAMIC = 'dynamic'

QUIZ_TYPE_CHOICES = (
    (CONFIGURED, _('Configured')),
    (DYNAMIC, _('Dynamic')),
)
