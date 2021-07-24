from django.views import generic
from django.contrib.auth import mixins as auth_mixins

from apps.categories import models as categories_models


class IndexView(auth_mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = categories_models.Category.objects.filter(
            is_public=True, depth=1,
        )
        return context


class AboutUsView(auth_mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'home/about-us.html'
