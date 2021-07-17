from django.views import generic
from django.contrib.auth import mixins as auth_mixins


class CategoriesIndexView(auth_mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'categories/index.html'


class CategoriesListView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'categories/index.html'


class CategoriesCreateView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'categories/index.html'


class CategoriesUpdateView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'categories/index.html'


class CategoriesDetailView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'categories/index.html'


class CategoriesDeleteView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'categories/index.html'
