import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

from django_extensions.db.models import TimeStampedModel

from . import constants as questions_constants
from . import managers as questions_managers


class Question(TimeStampedModel):
    language = models.ForeignKey('languages.Language', verbose_name=_('Language'), on_delete=models.CASCADE)
    category = models.ForeignKey('categories.Category', verbose_name=_('Category'),
                                 null=True, blank=True, on_delete=models.CASCADE)
    sentence = models.ForeignKey('sentences.Sentence', verbose_name=_('Sentence'),
                                 related_name='questions', on_delete=models.CASCADE)
    description = models.TextField(
        verbose_name=_("Description"),
        blank=True, help_text=_("A description of the Question"))
    question_type = models.CharField(verbose_name=_('Question type'),
                                     max_length=16, choices=questions_constants.QUESTION_TYPE_CHOICES,
                                     default=questions_constants.MCQ, db_index=True)
    maximum_number_of_choices = models.PositiveIntegerField(_("Maximum number of choices"), default=4)
    maximum_marks = models.DecimalField(_('Maximum Marks'), default=4, decimal_places=2, max_digits=6)
    correct_answer = models.ForeignKey('sentences.Sentence', verbose_name=_('Correct answer'),
                                       related_name='questions_correct_answers', on_delete=models.CASCADE,
                                       null=True, blank=True)
    success_text = models.TextField(
        verbose_name=_("Success text"),
        blank=True, help_text=_("A message that will be shown after successfully answering the question."))
    hint_text = models.TextField(
        verbose_name=_("Hint text"),
        blank=True, help_text=_("A message that will be shown if this question is not answered correctly."))
    is_published = models.BooleanField(_('Has been published?'), default=False, null=False)
    display_order = models.PositiveIntegerField(_("Display order"), default=0)

    is_deleted = models.BooleanField(_('Is Deleted?'), default=False, db_index=True)
    date_removed = models.DateTimeField(null=True, blank=True, db_index=True)

    objects = questions_managers.QuestionManager()

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')

    def __str__(self):
        return self.sentence.text

    def delete(self, **kwargs):
        self.is_deleted = True
        self.date_removed = timezone.now()
        self.save()

    def is_choice_question(self):
        return self.question_type in questions_constants.CHOICE_QUESTION_TYPES

    def is_text_question(self):
        return self.question_type in questions_constants.TEXT_QUESTION_TYPES

    def get_correct_choice(self):
        return self.choices.filter(is_correct=True).first()

    def get_correct_text(self):
        return self.correct_answer.text

    def get_answer_text(self):
        answer_text = ''
        if self.is_text_question():
            answer_text = self.correct_answer.text
        elif self.is_choice_question():
            choice = self.get_correct_choice()
            if choice:
                answer_text = choice.sentence.text
        return answer_text


class Choice(TimeStampedModel):
    language = models.ForeignKey('languages.Language', verbose_name=_('Language'), on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    sentence = models.ForeignKey('sentences.Sentence', verbose_name=_('Sentence'), on_delete=models.CASCADE)
    is_correct = models.BooleanField(_('Is this answer correct?'), default=False, null=False)
    is_deleted = models.BooleanField(_('Is Deleted?'), default=False, db_index=True)
    date_removed = models.DateTimeField(null=True, blank=True)

    objects = questions_managers.ChoiceManager()

    class Meta:
        verbose_name = _('Choice')
        verbose_name_plural = _('Choices')

    def __str__(self):
        return f"""
            language: {self.language.name},
            question: {self.question.sentence.text},
            sentence: {self.sentence.text},
            is_correct: {self.is_correct}
        """

    def delete(self, **kwargs):
        self.is_deleted = True
        self.date_removed = timezone.now()
        self.save()


class QuestionSet(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    title = models.CharField(verbose_name=_("Title"), max_length=64,
                             blank=False)
    description = models.TextField(
        verbose_name=_("Description"),
        blank=True, help_text=_("A description of the QuestionSet"))
    categories = models.ManyToManyField('categories.Category', blank=True)
    display_order = models.PositiveIntegerField(_("Display order"), default=0)

    is_deleted = models.BooleanField(_('Is Deleted?'), default=False, db_index=True)
    date_removed = models.DateTimeField(null=True, blank=True, db_index=True)

    objects = questions_managers.QuestionSetManager()

    class Meta:
        verbose_name = _('Question set')
        verbose_name_plural = _('Question sets')

    def __str__(self):
        return self.title

    def delete(self, **kwargs):
        self.is_deleted = True
        self.date_removed = timezone.now()
        self.save()

    def get_questions_queryset(self):
        category_ids = []
        for category in self.categories.filter(is_active=True):
            category_ids.extend(list(category.get_descendants_and_self().values_list('id', flat=True)))
        category_ids = list(set(category_ids))
        return Question.objects.filter(category__in=category_ids)
