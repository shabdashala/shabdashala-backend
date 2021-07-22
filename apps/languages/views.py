from django.views import generic
from django.contrib.auth import mixins as auth_mixins


class LanguageIndexView(auth_mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'languages/index.html'


class LanguageListView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'languages/index.html'


class LanguageCreateView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'languages/index.html'


class LanguageUpdateView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'languages/index.html'


class LanguageDetailView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'languages/index.html'


class LanguageDeleteView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'languages/index.html'
