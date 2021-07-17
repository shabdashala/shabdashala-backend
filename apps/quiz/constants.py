from django.utils.translation import gettext as _

CONFIGURED = 'configured'
DYNAMIC = 'dynamic'

QUIZ_TYPE_CHOICES = (
    (CONFIGURED, _('Configured')),
    (DYNAMIC, _('Dynamic')),
)

MCQ = 'mcq'  # multiple choice answer question
MCMQ = 'mcmq'  # multiple choice multiple answer question
SWQ = 'swq'  # single word answer question
JWQ = 'jwq'  # jumbled word answer question
TRQ = 'tq'  # translation question

QUESTION_TYPE_CHOICES = (
    (MCQ, _('Multiple choice answer question')),
    (MCMQ, _('Multiple choice multiple answer question')),
    (JWQ, _('Jumbled word answer question')),
    (TRQ, _('Translation question')),
)

ALLOWED_NUMBER_OF_CORRECT_CHOICES = 1
MAX_CHOICES_COUNT = 4
