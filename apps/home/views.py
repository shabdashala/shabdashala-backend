from django.views import generic
from django.contrib.auth import mixins as auth_mixins

# from apps.categories import models as categories_models
from apps.quiz_attempts import models as quiz_attempts_models
from apps.quizzes import models as quizzes_models


class IndexView(auth_mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['categories'] = categories_models.Category.objects.filter(
        #     is_public=True, depth=1,
        # )
        context['quizzes'] = quizzes_models.Quiz.objects.filter(
            is_published=True)
        return context


class PracticeView(auth_mixins.LoginRequiredMixin, generic.DetailView):
    template_name = 'home/practice.html'
    model = quizzes_models.Quiz
    context_object_name = 'quiz'
    slug_field = 'uuid'
    slug_url_kwarg = 'quiz_uuid'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz_attempt'] = quiz_attempts_models.QuizAttempt.create_quiz_attempt(
            self.request.user, context['quiz'])
        context['quiz_attempt_question'] = context['quiz_attempt'].get_or_generate_next_question()
        context['quiz_attempt_question_number'] = context['quiz_attempt'].current_question_number
        return context


class AboutUsView(auth_mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'home/about-us.html'
