from django.views import generic
from django.contrib.auth import mixins as auth_mixins

from . import models as sentences_models


class SentenceIndexView(auth_mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'sentences/index.html'


class SentenceListView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'sentences/list.html'
    model = sentences_models.Sentence


class SentenceCreateView(auth_mixins.LoginRequiredMixin, generic.CreateView):
    template_name = 'sentences/index.html'


class SentenceUpdateView(auth_mixins.LoginRequiredMixin, generic.UpdateView):
    template_name = 'sentences/index.html'


class SentenceDetailView(auth_mixins.LoginRequiredMixin, generic.DetailView):
    template_name = 'sentences/detail.html'
    model = sentences_models.Sentence


class SentenceDeleteView(auth_mixins.LoginRequiredMixin, generic.DeleteView):
    template_name = 'sentences/index.html'
