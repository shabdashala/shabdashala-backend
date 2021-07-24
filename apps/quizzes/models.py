import uuid

from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.translation import gettext as _

from django_extensions.db.models import TimeStampedModel

from . import constants as quiz_constants


class Quiz(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    title = models.CharField(verbose_name=_("Title"), max_length=64,
                             blank=False)
    description = models.TextField(
        verbose_name=_("Description"),
        blank=True, help_text=_("A description of the quiz"))
    language = models.ForeignKey('languages.Language', verbose_name=_('Language'), on_delete=models.CASCADE)
    category = models.ForeignKey('categories.Category', verbose_name=_('Category'), on_delete=models.CASCADE)
    quiz_type = models.CharField(verbose_name=_('Quiz type'),
                                 max_length=16, choices=quiz_constants.QUIZ_TYPE_CHOICES,
                                 default=quiz_constants.DYNAMIC, db_index=True)
    maximum_number_of_questions = models.PositiveIntegerField(_('Maximum number of questions'), default=10)
    maximum_marks = models.PositiveIntegerField(_('Maximum marks'), default=10)
    maximum_bonus_marks = models.PositiveIntegerField(_('Maximum bonus marks'), default=10)
    is_published = models.BooleanField(_('Has been published?'), default=False, null=False)
    display_order = models.PositiveIntegerField(_("Display order"))
    random_order = models.BooleanField(
        blank=False, default=False,
        verbose_name=_("Random Order"),
        help_text=_("Display the questions in "
                    "a random order or as they "
                    "are set?"))
    pass_mark = models.SmallIntegerField(
        blank=True, default=0,
        verbose_name=_("Pass Mark"),
        help_text=_("Percentage required to pass exam."),
        validators=[MaxValueValidator(100)])
    success_text = models.TextField(
        blank=True, help_text=_("Displayed if user passes."),
        verbose_name=_("Success Text"))
    fail_text = models.TextField(
        verbose_name=_("Fail Text"),
        blank=True, help_text=_("Displayed if user fails."))
    answers_at_end = models.BooleanField(
        blank=False, default=False,
        help_text=_("Correct answer is NOT shown after question."
                    " Answers displayed at the end."),
        verbose_name=_("Answers at end"))
    exam_paper = models.BooleanField(
        blank=False, default=False,
        help_text=_("If yes, the result of each"
                    " attempt by a user will be"
                    " stored. Necessary for marking."),
        verbose_name=_("Exam Paper"))
    ask_till_all_correct = models.BooleanField(
        blank=False, default=False,
        help_text=_("User should answer all questions."),
        verbose_name=_("Ask till all correct"))
    questions = models.ManyToManyField(to='questions.Question', through='QuizQuestion')
    question_set = models.ManyToManyField(to='questions.QuestionSet', through='QuizQuestionSet',
                                          blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'<Quiz: category={self.category.full_name}>'


class QuizQuestion(TimeStampedModel):
    quiz = models.ForeignKey('quizzes.Quiz', verbose_name=_('Quiz'), on_delete=models.CASCADE)
    question = models.ForeignKey('questions.Question', verbose_name=_('Quiz'), on_delete=models.CASCADE)
    display_order = models.PositiveIntegerField(_("Display order"))

    def __str__(self):
        return self.question.sentence.text


class QuizQuestionSet(TimeStampedModel):
    quiz = models.ForeignKey('quizzes.Quiz', verbose_name=_('Quiz'), on_delete=models.CASCADE)
    question_set = models.ForeignKey('questions.QuestionSet', verbose_name=_('Quiz Set'), on_delete=models.CASCADE)
    display_order = models.PositiveIntegerField(_("Display order"))

    def __str__(self):
        return self.question_set.title