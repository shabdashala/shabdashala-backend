import typing

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import generic

from apps.categories import models as categories_models
from apps.questions import models as questions_models
from apps.quiz_attempts import forms as quiz_attempts_forms
from apps.quiz_attempts import models as quiz_attempts_models
from apps.quizzes import models as quizzes_models


User = get_user_model()


class PrivacyPolicyView(generic.TemplateView):
    template_name = 'home/privacy-policy.html'


class ProfileView(generic.DetailView):
    template_name = 'home/profile.html'
    model = get_user_model()
    slug_field = 'username'
    slug_url_kwarg = 'username'
    # renaming context object name to respect auth template context processor
    # `django.contrib.auth.context_processors.auth`
    context_object_name = 'user_obj'


class IndexView(generic.TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = categories_models.Category.objects.filter(
            is_public=True, depth=1,
        )
        context['quizzes'] = quizzes_models.Quiz.objects.filter(
            is_published=True)
        return context


class AboutUsView(generic.TemplateView):
    template_name = 'home/about-us.html'


class LeaderBoardView(generic.ListView):
    template_name = 'home/leaderboard.html'
    model = quiz_attempts_models.QuizAttempt
    context_object_name = 'quiz_attempts'
    ordering = ['-completed_at', '-id']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            is_abandoned=False,
            is_completed=True,
            is_deleted=False)
        return queryset


class PracticeViewMixin(object):
    quiz: typing.Union[None, quizzes_models.Quiz] = None
    quiz_attempt: typing.Union[None, quiz_attempts_models.QuizAttempt] = None

    attempts_complete_template_name = 'home/practice/attempts_complete.html'
    number_of_attempts: typing.Union[None, int] = None
    has_completed_attempts: typing.Union[None, bool] = None

    quiz_attempt_model = quiz_attempts_models.QuizAttempt

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.quiz = get_object_or_404(
            quizzes_models.Quiz,
            uuid=kwargs['quiz_uuid'],
            is_published=True
        )
        # fifteen_minutes_ago = timezone.now() - timezone.timedelta(minutes=15)
        self.number_of_attempts = self.quiz_attempt_model.objects.filter(
            user=request.user,
            quiz=self.quiz,
            is_completed=True,
            # created__gte=fifteen_minutes_ago,
        ).count()

        allowed_max_user_attemps = self.quiz.maximum_number_of_user_attempts

        if self.number_of_attempts \
                and self.number_of_attempts >= allowed_max_user_attemps:
            self.has_completed_attempts = True
        if not self.has_completed_attempts:
            self.quiz_attempt = self.get_quiz_attempt()
        if self.quiz_attempt and self.quiz_attempt.is_completed:
            return redirect(self.quiz_attempt.get_practice_results_url())
        return super().dispatch(request, *args, **kwargs)

    def get_quiz_attempt(self):
        raise NotImplementedError('child class should implement this method')


class PracticeStartView(PracticeViewMixin, generic.DetailView):
    template_name = 'home/practice/start.html'
    model = quizzes_models.Quiz
    context_object_name = 'quiz'
    slug_field = 'uuid'
    slug_url_kwarg = 'quiz_uuid'
    start_new_action = 'start-new'
    quiz_attempt_model = quiz_attempts_models.QuizAttempt

    def get_quiz_attempt(self):
        # fifteen_minutes_ago = timezone.now() - timezone.timedelta(minutes=15)
        return self.quiz_attempt_model.objects.filter(
            user=self.request.user,
            quiz=self.quiz,
            is_completed=False,
            is_abandoned=False,
            # created__gte=fifteen_minutes_ago,
        ).first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = {}
        if self.quiz_attempt:
            extra_context = {
                'quiz_attempt': self.quiz_attempt
            }
        return dict(context,
                    start_new_action=self.start_new_action,
                    **extra_context)

    def get_template_names(self):
        if self.has_completed_attempts:
            return [self.attempts_complete_template_name]
        return [self.template_name]

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        if action == self.start_new_action:
            existing_attempts = self.quiz_attempt_model.objects.filter(
                user=self.request.user,
                quiz=self.quiz,
                is_completed=False,
                is_abandoned=False,
            )
            if existing_attempts.exists():
                existing_attempts.update(
                    is_abandoned=True,
                    abandoned_at=timezone.now())
            new_quiz_attempt = self.quiz_attempt_model.create_quiz_attempt(
                self.request.user, self.quiz)
            messages.success(request, _('Started new quiz'))
            return redirect(to=new_quiz_attempt.get_practice_home_url())
        return self.get(request, *args, **kwargs)


class PracticeProgressView(PracticeViewMixin, generic.FormView):
    form_class = quiz_attempts_forms.QuizQuestionForm
    progress_template_name = 'home/practice/progress.html'
    result_template_name = 'home/practice/results.html'
    quiz_attempt_question: typing.Union[
        None, quiz_attempts_models.AttemptedQuestion
    ] = None

    def get_quiz_attempt(self):
        return get_object_or_404(
            quiz_attempts_models.QuizAttempt, user=self.request.user,
            quiz=self.quiz, uuid=self.kwargs.get('quiz_attempt_uuid'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = {}
        if self.quiz_attempt:
            extra_context = {
                'quiz': self.quiz,
                'quiz_attempt': self.quiz_attempt,
                'quiz_attempt_question': self.quiz_attempt_question,
            }
        return dict(context, **extra_context)

    def get_template_names(self):
        if self.quiz_attempt.is_completed:
            return [self.result_template_name]
        elif self.has_completed_attempts:
            return [self.attempts_complete_template_name]
        return [self.progress_template_name]

    def get_success_url(self):
        return self.quiz_attempt.get_practice_home_url()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return dict(kwargs, instance=self.quiz_attempt_question.question)

    def get_form(self, *args, **kwargs):
        self.quiz_attempt_question = \
            self.quiz_attempt.get_or_generate_next_question()
        return self.form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        if self.quiz_attempt_question.question.is_choice_question():
            selected_choice = form.cleaned_data['choices']
            self.quiz_attempt_question.set_selected_choice(
                selected_choice=selected_choice)
        if not self.quiz_attempt.is_completed:
            messages.success(self.request, _('Correct'))
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.quiz_attempt_question.question.is_choice_question():
            selected_choice_id = form.data.get('choices')
            selected_choice = questions_models.Choice.objects.filter(
                id=selected_choice_id
            ).first()
            self.quiz_attempt_question.set_selected_choice(
                selected_choice=selected_choice)

        if not self.quiz_attempt.is_completed:
            messages.error(self.request, _('Wrong'))
        return redirect(self.get_success_url())


class PracticeResultsView(generic.DetailView):
    template_name = 'home/practice/results.html'
    model = quizzes_models.Quiz
    context_object_name = 'quiz'
    slug_field = 'uuid'
    slug_url_kwarg = 'quiz_uuid'

    quiz = None
    quiz_attempt = None

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.quiz = get_object_or_404(
            quizzes_models.Quiz,
            uuid=kwargs['quiz_uuid'],
            is_published=True
        )
        self.quiz_attempt = get_object_or_404(
            quiz_attempts_models.QuizAttempt, user=self.request.user,
            quiz=self.quiz, uuid=self.kwargs.get('quiz_attempt_uuid'))
        if self.quiz_attempt and self.quiz_attempt.is_completed is False:
            return redirect(self.quiz_attempt.get_practice_home_url())
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = {}
        if self.quiz_attempt:
            extra_context = {
                'quiz': self.quiz,
                'quiz_attempt': self.quiz_attempt,
            }
        return dict(context, **extra_context)
