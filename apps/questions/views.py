from django.views import generic
from django.contrib.auth import mixins as auth_mixins


class QuestionIndexView(auth_mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'questions/index.html'


class QuestionListView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'questions/list.html'


class QuestionCreateView(auth_mixins.LoginRequiredMixin, generic.CreateView):
    template_name = 'questions/form.html'


class QuestionUpdateView(auth_mixins.LoginRequiredMixin, generic.UpdateView):
    template_name = 'questions/form.html'


class QuestionDetailView(auth_mixins.LoginRequiredMixin, generic.DetailView):
    template_name = 'questions/detail.html'


class QuestionDeleteView(auth_mixins.LoginRequiredMixin, generic.DeleteView):
    template_name = 'questions/delete.html'
