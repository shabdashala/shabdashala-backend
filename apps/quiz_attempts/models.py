import random

from django.conf import settings
from django.core.validators import (
    validate_comma_separated_integer_list,
)
from django.db import models, transaction
from django.contrib.postgres import fields as postgres_fields
from django.utils import timezone
from django.utils.translation import gettext as _

from django_extensions.db.models import TimeStampedModel

from apps.questions import models as questions_models


class QuizAttempt(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'), on_delete=models.CASCADE)
    quiz = models.ForeignKey('quizzes.Quiz', verbose_name=_('Quiz'), on_delete=models.CASCADE)
    questions_list = postgres_fields.ArrayField(
        models.IntegerField(),
        size=40,
        verbose_name=_("Questions list"),
        validators=[validate_comma_separated_integer_list])
    completed_question_list = postgres_fields.ArrayField(
        models.IntegerField(),
        size=40,
        verbose_name=_("Completed question list"),
        validators=[validate_comma_separated_integer_list])
    not_completed_question_list = postgres_fields.ArrayField(
        models.IntegerField(),
        size=40,
        verbose_name=_("Not completed question list"),
        validators=[validate_comma_separated_integer_list])
    incorrect_question_list = postgres_fields.ArrayField(
        models.IntegerField(),
        size=40,
        blank=True,
        verbose_name=_("Incorrect questions list"),
        validators=[validate_comma_separated_integer_list])

    total_score = models.DecimalField(_('Total Score'), default=0, decimal_places=2, max_digits=10)
    current_score = models.DecimalField(_('Current Score'), default=0, decimal_places=2, max_digits=10)

    is_completed = models.BooleanField(default=False, blank=False,
                                       verbose_name=_("Is completed?"))
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Completed Date and time?"))
    final_submission_info = models.JSONField(verbose_name=_(" info"), default=dict)

    def __str__(self):
        return f'<QuizAttempt: user={self.user}>'

    def get_new_question(self):
        question = None
        question_id = None
        if self.not_completed_question_list:
            question_id = self.not_completed_question_list[0]
        elif self.quiz.ask_till_all_correct and self.incorrect_question_list:
            question_id = self.incorrect_question_list[0]
        if question_id:
            question = questions_models.Question.objects.filter(
                id=question_id).first()
        return question

    @transaction.atomic()
    def update_score(self, **kwargs):
        marks_sum = self.attempted_questions.filter(is_correct=True).aggregate(
            models.Sum('marks_obtained'))['marks_obtained__sum']
        if kwargs.get('is_completed'):
            self.is_completed = marks_sum or 0
        self.total_score = marks_sum or 0
        self.save()


class AttemptedQuestion(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'), on_delete=models.CASCADE)
    quiz_attempt = models.ForeignKey('QuizAttempt', on_delete=models.CASCADE, related_name='attempted_questions')
    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE)
    selected_choice = models.ForeignKey('questions.Choice', on_delete=models.CASCADE, null=True, blank=True)
    entered_text = models.ForeignKey('sentences.Sentence', verbose_name=_('Sentence'),
                                     on_delete=models.CASCADE, null=True, blank=True)
    is_correct = models.BooleanField(_('Was this attempt correct?'), default=False, null=False)
    marks_obtained = models.DecimalField(_('Marks Obtained'), default=0, decimal_places=2, max_digits=6)

    is_evaluated = models.BooleanField(default=False, blank=False,
                                       verbose_name=_("Is evaluated?"))
    evaluated_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Completed Date and time?"))
    final_submission_info = models.JSONField(verbose_name=_(" info"), default=dict)

    def get_absolute_url(self):
        return f'/attempted-result/{self.pk}/'

    @transaction.atomic()
    def evaluate_question(self):
        is_correct = False
        is_valid_choice_question = self.question.is_choice_question() and \
            self.question.id == self.selected_choice.question_id
        is_valid_text_question = self.question.is_text_question() and \
            self.question.correct_answer and self.entered_text

        if not self.is_evaluated or not is_valid_choice_question or not is_valid_text_question:
            pass

        elif self.question.is_choice_question():
            is_correct = self.selected_choice in self.question.choices.filter(is_correct=True)

        elif self.question.is_text_question():
            normalized_correct_answer_text = self.question.correct_answer.text.lower()
            normalized_user_entered_text = self.entered_text.text.lower()
            if normalized_user_entered_text == normalized_correct_answer_text:
                is_correct = True

        if is_correct:
            self.marks_obtained = self.question.maximum_marks
            self.is_correct = True
            self.evaluated_at = timezone.now()
            self.save()
            self.quiz_attempt.update_score()

    def get_submitted_final_info(self):
        return {
            'question': {
                'pk': self.question.id,
                'text': self.question.id,
            }
        }
