from django.views import generic
from django.contrib.auth import mixins as auth_mixins


class QuizAttemptIndexView(auth_mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'quiz_attempts/index.html'


class QuizAttemptListView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'quiz_attempts/list.html'


class QuizAttemptCreateView(auth_mixins.LoginRequiredMixin, generic.CreateView):
    template_name = 'quiz_attempts/form.html'


class QuizAttemptUpdateView(auth_mixins.LoginRequiredMixin, generic.UpdateView):
    template_name = 'quiz_attempts/form.html'


class QuizAttemptDetailView(auth_mixins.LoginRequiredMixin, generic.DetailView):
    template_name = 'quiz_attempts/detail.html'


class QuizAttemptDeleteView(auth_mixins.LoginRequiredMixin, generic.DeleteView):
    template_name = 'quiz_attempts/delete.html'
