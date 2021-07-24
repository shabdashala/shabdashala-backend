from django.utils.translation import gettext as _

MCQ = 'mcq'  # multiple choice answer question
MCMQ = 'mcmq'  # multiple choice multiple answer question
JWQ = 'jwq'  # jumbled word answer question
SWQ = 'swq'  # single word answer question
TRQ = 'trq'  # translation question
TQ = 'tq'  # textual question

QUESTION_TYPE_CHOICES = (
    (MCQ, _('Multiple choice answer question')),
    (MCMQ, _('Multiple choice multiple answer question')),
    (JWQ, _('Jumble words answer question')),
    (SWQ, _('Single word answer question')),
    (TRQ, _('Translation question')),
    (TQ, _('Textual question')),
)

CHOICE_QUESTION_TYPES = [MCQ, MCMQ]
TEXT_QUESTION_TYPES = [JWQ, TRQ, TQ]

ALLOWED_NUMBER_OF_CORRECT_CHOICES = 1
MAX_CHOICES_COUNT = 4
