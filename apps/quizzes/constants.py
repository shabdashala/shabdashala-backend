from django.utils.translation import gettext as _

ADAPTIVE = 'adaptive'
CONFIGURED = 'configured'
DYNAMIC = 'dynamic'


QUIZ_TYPE_CHOICES = (
    (ADAPTIVE, _('Adaptive')),
    (CONFIGURED, _('Configured')),
    (DYNAMIC, _('Dynamic')),
)
