from django.views import generic
from django.contrib.auth import mixins as auth_mixins

from . import models as word_models


class WordIndexView(auth_mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'words/index.html'


class WordListView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'words/list.html'
    model = word_models.Word


class WordCreateView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'words/form.html'
    model = word_models.Word


class WordUpdateView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'words/index.html'


class WordDetailView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'words/index.html'


class WordDeleteView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'words/index.html'
