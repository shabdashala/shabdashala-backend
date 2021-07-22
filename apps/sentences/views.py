from django.views import generic
from django.contrib.auth import mixins as auth_mixins


class SentenceIndexView(auth_mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'sentences/index.html'


class SentenceListView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'sentences/index.html'


class SentenceCreateView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'sentences/index.html'


class SentenceUpdateView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'sentences/index.html'


class SentenceDetailView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'sentences/index.html'


class SentenceDeleteView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'sentences/index.html'
