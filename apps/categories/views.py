from django.views import generic
from django.contrib.auth import mixins as auth_mixins


class CategoryIndexView(auth_mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'categories/index.html'


class CategoryListView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'categories/index.html'


class CategoryCreateView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'categories/index.html'


class CategoryUpdateView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'categories/index.html'


class CategoryDetailView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'categories/index.html'


class CategoryDeleteView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'categories/index.html'
