from django.views import generic
from django.contrib.auth import mixins as auth_mixins

from . import models as categories_models


class CategoryIndexView(auth_mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'categories/index.html'


class CategoryListView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'categories/index.html'


class CategoryCreateView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'categories/index.html'


class CategoryUpdateView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'categories/index.html'


class CategoryDetailView(auth_mixins.LoginRequiredMixin, generic.DetailView):
    template_name = 'categories/detail.html'
    model = categories_models.Category

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True, is_public=True)
        return queryset


class CategoryDeleteView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'categories/index.html'
