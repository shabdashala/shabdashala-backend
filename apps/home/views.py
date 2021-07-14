from django.views import generic
from django.contrib.auth import mixins as auth_mixins


class IndexView(auth_mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'home/index.html'


