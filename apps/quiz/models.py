import uuid
import random

from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.translation import gettext as _

from django_extensions.db.models import TimeStampedModel

from . import constants as quiz_constants


class Quiz(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
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

    questions = models.ManyToManyField(to='Question', through='QuizQuestion')

    def __str__(self):
        return f'<Quiz: category={self.category.full_name}>'


class Question(TimeStampedModel):
    language = models.ForeignKey('languages.Language', verbose_name=_('Language'), on_delete=models.CASCADE)
    category = models.ForeignKey('categories.Category', verbose_name=_('Category'),
                                 null=True, blank=True, on_delete=models.CASCADE)
    sentence = models.ForeignKey('sentences.Sentence', verbose_name=_('Sentence'), on_delete=models.CASCADE)
    question_type = models.CharField(verbose_name=_('Question type'),
                                     max_length=16, choices=quiz_constants.QUESTION_TYPE_CHOICES,
                                     default=quiz_constants.DYNAMIC, db_index=True)
    maximum_marks = models.DecimalField(_('Maximum Marks'), default=4, decimal_places=2, max_digits=6)
    is_published = models.BooleanField(_('Has been published?'), default=False, null=False)

    def __str__(self):
        return self.sentence.text


class Choice(TimeStampedModel):
    language = models.ForeignKey('languages.Language', verbose_name=_('Language'), on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    sentence = models.ForeignKey('sentences.Sentence', verbose_name=_('Sentence'), on_delete=models.CASCADE)
    is_correct = models.BooleanField(_('Is this answer correct?'), default=False, null=False)

    def __str__(self):
        return self.sentence


class QuizQuestion(TimeStampedModel):
    quiz = models.ForeignKey('quiz.Quiz', verbose_name=_('Quiz'), on_delete=models.CASCADE)
    question = models.ForeignKey('quiz.Question', verbose_name=_('Quiz'), on_delete=models.CASCADE)
    display_order = models.PositiveIntegerField(_("Display order"))

    def __str__(self):
        return self.question


class UserAttemptedQuiz(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'), on_delete=models.CASCADE)
    quiz = models.ForeignKey('quiz.Quiz', verbose_name=_('Quiz'), on_delete=models.CASCADE)
    total_score = models.DecimalField(_('Total Score'), default=0, decimal_places=2, max_digits=10)

    def __str__(self):
        return f'<QuizProfile: user={self.user}>'

    def get_new_question(self):
        used_questions_pk = UserAttemptedQuestion.objects.filter(user_quiz=self).values_list('question__pk', flat=True)
        remaining_questions = Question.objects.exclude(pk__in=used_questions_pk)
        if not remaining_questions.exists():
            return
        return random.choice(remaining_questions)

    def create_attempt(self, question):
        attempted_question = UserAttemptedQuestion(question=question, quiz_profile=self)
        attempted_question.save()

    def evaluate_attempt(self, attempted_question, selected_choice):
        if attempted_question.question_id != selected_choice.question_id:
            return

        attempted_question.selected_choice = selected_choice
        if selected_choice.is_correct is True:
            attempted_question.is_correct = True
            attempted_question.marks_obtained = attempted_question.question.maximum_marks

        attempted_question.save()
        self.update_score()

    def update_score(self):
        marks_sum = self.attempted_questions.filter(is_correct=True).aggregate(
            models.Sum('marks_obtained'))['marks_obtained__sum']
        self.total_score = marks_sum or 0
        self.save()


class UserAttemptedQuestion(TimeStampedModel):
    user_attempted_quiz = models.ForeignKey(UserAttemptedQuiz, on_delete=models.CASCADE,
                                            related_name='attempted_questions')
    quiz_question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True)
    is_correct = models.BooleanField(_('Was this attempt correct?'), default=False, null=False)
    marks_obtained = models.DecimalField(_('Marks Obtained'), default=0, decimal_places=2, max_digits=6)

    def get_absolute_url(self):
        return f'/submission-result/{self.pk}/'
