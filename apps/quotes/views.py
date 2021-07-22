from django.views import generic
from django.contrib.auth import mixins as auth_mixins


class QuoteIndexView(auth_mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'quotes/index.html'


class QuoteListView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'quotes/list.html'


class QuoteCreateView(auth_mixins.LoginRequiredMixin, generic.CreateView):
    template_name = 'quotes/form.html'


class QuoteUpdateView(auth_mixins.LoginRequiredMixin, generic.UpdateView):
    template_name = 'quotes/form.html'


class QuoteDetailView(auth_mixins.LoginRequiredMixin, generic.DetailView):
    template_name = 'quotes/detail.html'


class QuoteDeleteView(auth_mixins.LoginRequiredMixin, generic.DeleteView):
    template_name = 'quotes/delete.html'
