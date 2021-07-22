from django.views import generic
from django.contrib.auth import mixins as auth_mixins


class WordIndexView(auth_mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'words/index.html'


class WordListView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'words/index.html'


class WordCreateView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'words/index.html'


class WordUpdateView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'words/index.html'


class WordDetailView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'words/index.html'


class WordDeleteView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'words/index.html'
