from django.views import generic
from django.contrib.auth import mixins as auth_mixins


class SentencesIndexView(auth_mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'sentences/index.html'


class SentencesListView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'sentences/index.html'


class SentencesCreateView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'sentences/index.html'


class SentencesUpdateView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'sentences/index.html'


class SentencesDetailView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'sentences/index.html'


class SentencesDeleteView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'sentences/index.html'
