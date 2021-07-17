from django.views import generic
from django.contrib.auth import mixins as auth_mixins


class LanguagesIndexView(auth_mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'languages/index.html'


class LanguagesListView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'languages/index.html'


class LanguagesCreateView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'languages/index.html'


class LanguagesUpdateView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'languages/index.html'


class LanguagesDetailView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'languages/index.html'


class LanguagesDeleteView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'languages/index.html'
