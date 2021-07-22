from django.views import generic
from django.contrib.auth import mixins as auth_mixins


class QuizIndexView(auth_mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'quiz/index.html'


class QuizListView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'quiz/list.html'


class QuizCreateView(auth_mixins.LoginRequiredMixin, generic.CreateView):
    template_name = 'quiz/form.html'


class QuizUpdateView(auth_mixins.LoginRequiredMixin, generic.UpdateView):
    template_name = 'quiz/form.html'


class QuizDetailView(auth_mixins.LoginRequiredMixin, generic.DetailView):
    template_name = 'quiz/detail.html'


class QuizDeleteView(auth_mixins.LoginRequiredMixin, generic.DeleteView):
    template_name = 'sentences/index.html'


class QuizQuestionCreateView(auth_mixins.LoginRequiredMixin, generic.CreateView):
    template_name = 'quiz/questions/form.html'


class QuizQuestionUpdateView(auth_mixins.LoginRequiredMixin, generic.UpdateView):
    template_name = 'quiz/questions/form.html'


class QuizQuestionDetailView(auth_mixins.LoginRequiredMixin, generic.DetailView):
    template_name = 'quiz/questions/detail.html'


class QuizQuestionDeleteView(auth_mixins.LoginRequiredMixin, generic.DeleteView):
    template_name = 'sentences/index.html'
