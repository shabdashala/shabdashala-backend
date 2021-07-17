from django.views import generic
from django.contrib.auth import mixins as auth_mixins


class WordsIndexView(auth_mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'words/index.html'


class WordsListView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'words/index.html'


class WordsCreateView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'words/index.html'


class WordsUpdateView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'words/index.html'


class WordsDetailView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'words/index.html'


class WordsDeleteView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'words/index.html'
