import copy
import random
import typing
import uuid

from django.conf import settings
from django.core.validators import (
    validate_comma_separated_integer_list,
)
from django.db import models, transaction
from django.db.models.query import QuerySet
from django.contrib.postgres import fields as postgres_fields
from django.utils import timezone
from django.utils.translation import gettext as _

from django_extensions.db.models import TimeStampedModel
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField

from apps.questions import models as questions_models
from apps.quizzes import constants as quizzes_constants


class QuizAttempt(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'), on_delete=models.CASCADE)
    quiz = models.ForeignKey('quizzes.Quiz', verbose_name=_('Quiz'), on_delete=models.CASCADE)
    questions_list = postgres_fields.ArrayField(
        models.IntegerField(),
        size=40,
        verbose_name=_("Questions list"),
        validators=[validate_comma_separated_integer_list],
        null=True, blank=True)
    completed_question_list = postgres_fields.ArrayField(
        models.IntegerField(),
        size=40,
        verbose_name=_("Completed question list"),
        validators=[validate_comma_separated_integer_list],
        null=True, blank=True)
    not_completed_question_list = postgres_fields.ArrayField(
        models.IntegerField(),
        size=40,
        verbose_name=_("Not completed question list"),
        validators=[validate_comma_separated_integer_list],
        null=True, blank=True)
    incorrect_question_list = postgres_fields.ArrayField(
        models.IntegerField(),
        size=40,
        verbose_name=_("Incorrect questions list"),
        validators=[validate_comma_separated_integer_list],
        null=True, blank=True)

    total_score = models.DecimalField(_('Total Score'), default=0, decimal_places=2, max_digits=10)
    current_score = models.DecimalField(_('Current Score'), default=0, decimal_places=2, max_digits=10)
    is_abandoned = models.BooleanField(default=False, blank=False,
                                       verbose_name=_("Is Abandoned?"))
    is_completed = models.BooleanField(default=False, blank=False,
                                       verbose_name=_("Is completed?"))
    abandoned_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Abandoned Date and time?"))
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Completed Date and time?"))
    final_submission_info = models.JSONField(verbose_name=_(" info"), default=dict)

    created = CreationDateTimeField(_('created'), db_index=True)
    modified = ModificationDateTimeField(_('modified'), db_index=True)

    def __str__(self):
        return f'<QuizAttempt: user={self.user} quiz={self.quiz}>'

    @property
    def current_question_number(self):
        return len(self.completed_question_list or []) + 1

    @property
    def total_questions(self):
        return len(self.questions_list or [])

    @property
    def marks_percent(self):
        if self.current_score >= 0 and self.total_score > 0:
            return int(self.current_score / self.total_score)
        return 0

    @transaction.atomic()
    def add_to_questions_list(self, new_question_id):
        questions_list = copy.copy(self.questions_list) or []
        if new_question_id not in questions_list:
            questions_list.append(new_question_id)
            self.questions_list = questions_list
            self.save(update_fields=['questions_list'])

    @transaction.atomic()
    def add_to_completed_question_list(self, question_id):
        completed_question_list = copy.copy(self.completed_question_list) or []
        not_completed_question_list = copy.copy(self.not_completed_question_list) or []

        if question_id not in completed_question_list:
            completed_question_list.append(question_id)
            self.completed_question_list = completed_question_list
            self.save(update_fields=['completed_question_list'])

        if question_id in not_completed_question_list:
            not_completed_question_list.remove(question_id)
            self.not_completed_question_list = not_completed_question_list
            self.save(update_fields=['not_completed_question_list'])

    @transaction.atomic()
    def add_to_not_completed_question_list(self, new_question_id):
        completed_question_list = copy.copy(self.completed_question_list) or []
        not_completed_question_list = copy.copy(self.not_completed_question_list) or []

        if new_question_id not in not_completed_question_list:
            not_completed_question_list.append(new_question_id)
            self.not_completed_question_list = not_completed_question_list
            self.save(update_fields=['not_completed_question_list'])

        if new_question_id in completed_question_list:
            completed_question_list.remove(new_question_id)
            self.completed_question_list = completed_question_list
            self.save(update_fields=['completed_question_list'])

    def get_base_questions_queryset(self):
        question_ids = set()
        questions_queryset = self.quiz.questions.filter(is_published=True)

        if questions_queryset.exists():
            for question in questions_queryset.iterator():
                question_ids.add(question.id)

        if self.quiz.question_sets.exists():
            for question_set in self.quiz.question_sets.iterator():
                for question in question_set.get_questions_queryset().iterator():
                    question_ids.add(question.id)

        return questions_models.Question.objects.filter(id__in=question_ids)

    def get_next_questions_queryset(self) -> typing.Union[QuerySet[questions_models.Question],
                                                          typing.Sequence[questions_models.Question]]:
        questions_list = self.questions_list or []
        completed_questions_list = self.completed_question_list or []
        not_completed_questions_list = self.not_completed_question_list or []
        incorrect_question_list = self.incorrect_question_list or []

        max_number_of_questions = self.quiz.maximum_number_of_questions
        questions_queryset = questions_models.Question.objects.none()

        if self.is_completed or len(completed_questions_list) == self.quiz.maximum_number_of_questions:
            pass

        elif len(questions_list) == max_number_of_questions and \
                incorrect_question_list and self.quiz.ask_till_all_correct:
            questions_queryset = questions_models.Question.objects.filter(
                id=questions_list, is_published=True)

        elif not_completed_questions_list:
            questions_queryset = questions_models.Question.objects.filter(
                id__in=self.not_completed_question_list, is_published=True)

        else:
            questions_queryset = self.get_base_questions_queryset()
        return questions_queryset

    def get_next_question(self) -> typing.Union[None, questions_models.Question]:
        questions_list = copy.copy(self.questions_list or [])
        completed_questions_list = copy.copy(self.completed_question_list or [])
        not_completed_questions_list = copy.copy(self.not_completed_question_list or [])

        next_question = None
        if self.quiz.quiz_type == quizzes_constants.DYNAMIC:
            if len(questions_list) == len(completed_questions_list) and \
                    len(questions_list) == self.quiz.maximum_number_of_questions:
                pass
            elif not_completed_questions_list:
                question_id = not_completed_questions_list[0]
                next_question = questions_models.Question.objects.filter(
                    id=question_id, is_published=True).first()
        else:
            questions_queryset = self.get_next_questions_queryset()
            next_question = random.choice(questions_queryset)
        return next_question

    @transaction.atomic()
    def get_or_generate_next_question(self) -> typing.Union[None, 'AttemptedQuestion']:
        new_question: typing.Union[None, questions_models.Question] = self.get_next_question()
        if new_question:
            if self.quiz.quiz_type == quizzes_constants.ADAPTIVE:
                self.add_to_questions_list(new_question.id)
            self.add_to_not_completed_question_list(new_question.id)

        new_attempted_question: typing.Union[None, 'AttemptedQuestion'] = None
        if new_question:
            if self.attempted_questions.filter(question=new_question).exists():
                new_attempted_question = self.attempted_questions.filter(question=new_question).first()
            else:
                new_attempted_question = self.create_attempted_question(question=new_question)
        return new_attempted_question

    @classmethod
    def create_quiz_attempt(cls, user, quiz):
        active_quiz_attempts = cls.objects.filter(user=user, quiz=quiz, is_completed=False, is_abandoned=False)
        if active_quiz_attempts.exists():
            quiz_attempt = active_quiz_attempts.first()
        else:
            quiz_attempt = cls.objects.create(user=user, quiz=quiz)
        if quiz_attempt.is_completed is False and \
                not quiz_attempt.questions_list and \
                quiz.quiz_type == quizzes_constants.DYNAMIC:
            question_ids = list(quiz_attempt.get_base_questions_queryset().values_list('id', flat=True))
            questions_list = random.sample(question_ids, quiz.maximum_number_of_questions)

            quiz_attempt.questions_list = copy.copy(questions_list)
            quiz_attempt.completed_question_list = []
            quiz_attempt.not_completed_question_list = copy.copy(questions_list)

            total_score = 0
            for correct_question in questions_models.Question.objects.filter(id__in=question_ids).iterator():
                total_score += correct_question.question.maximum_marks
            quiz_attempt.total_score = total_score

            quiz_attempt.save(update_fields=[
                'questions_list',
                'completed_question_list',
                'not_completed_question_list',
                'total_score',
            ])
        return quiz_attempt

    @transaction.atomic()
    def create_attempted_question(self, question: questions_models.Question,
                                  selected_choice: typing.Union[None, questions_models.Choice] = None):
        attempted_question = self.attempted_questions.create(
            user=self.user,
            question=question)
        if question.is_choice_question() and selected_choice:
            attempted_question.set_selected_choice(selected_choice=selected_choice)
        return attempted_question

    @transaction.atomic()
    def update_score(self, **kwargs):
        marks_sum = self.attempted_questions.filter(is_correct=True).aggregate(
            models.Sum('marks_obtained'))['marks_obtained__sum']
        if kwargs.get('is_completed'):
            self.is_completed = kwargs['is_completed']
        self.current_score = marks_sum or 0
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
    def set_selected_choice(self, selected_choice: questions_models.Choice):
        self.selected_choice = selected_choice
        self.save(update_fields=['selected_choice'])
        self.evaluate_question()

    @transaction.atomic()
    def evaluate_question(self):
        if self.is_evaluated or self.quiz_attempt.is_completed:
            return

        is_correct = False

        is_valid_choice_question = self.question.is_choice_question() and \
            self.selected_choice and \
            self.question.id == self.selected_choice.question_id
        is_valid_text_question = self.question.is_text_question() and \
            self.question.correct_answer and self.entered_text

        if is_valid_choice_question:
            if self.selected_choice:
                is_correct = self.selected_choice in self.question.choices.filter(is_correct=True)

        elif is_valid_text_question:
            normalized_correct_answer_text = self.question.correct_answer.text.lower()
            normalized_user_entered_text = self.entered_text.text.lower()
            if normalized_user_entered_text == normalized_correct_answer_text:
                is_correct = True

        self.marks_obtained = self.question.maximum_marks if is_correct else 0
        self.is_correct = is_correct
        self.is_evaluated = True
        self.evaluated_at = timezone.now()
        self.save()
        self.quiz_attempt.update_score()
        if is_correct or not self.quiz_attempt.quiz.ask_till_all_correct:
            self.quiz_attempt.add_to_completed_question_list(self.question_id)
        elif not is_correct:
            self.quiz_attempt.add_to_not_completed_question_list(self.question_id)
        questions_list = list(self.quiz_attempt.questions_list) or []
        completed_questions_list = list(self.quiz_attempt.completed_question_list) or []
        if len(questions_list) == len(completed_questions_list) and \
                len(completed_questions_list) == self.quiz_attempt.quiz.maximum_number_of_questions:
            quiz_attempt = self.quiz_attempt
            quiz_attempt.is_completed = True
            quiz_attempt.save(update_fields=['is_completed'])

    def get_submitted_final_info(self):
        return {
            'question': {
                'pk': self.question.id,
                'text': self.question.id,
            }
        }

    @property
    def user_answer_text(self):
        if self.question.is_choice_question() and self.selected_choice:
            return self.selected_choice.sentence.text
        elif self.question.is_text_question() and self.entered_text:
            return self.entered_text.text
        return ''
