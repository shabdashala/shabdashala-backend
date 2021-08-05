from django.views import generic
from django.contrib.auth import mixins as auth_mixins
from django.shortcuts import get_object_or_404

from apps.categories import models as categories_models
from . import models as questions_models


class QuestionIndexView(auth_mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'questions/index.html'


class QuestionListView(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'questions/list.html'
    model = questions_models.Question
    category = None
    context_object_name = 'questions'

    def dispatch(self, request, *args, **kwargs):
        if kwargs.get('category_pk'):
            self.category = get_object_or_404(categories_models.Category, pk=kwargs['category_pk'],
                                              is_public=True, is_active=True, is_deleted=False)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.model.objects.none()
        if self.category:
            queryset = self.model.objects.filter(
                category__in=self.category.get_descendants_and_self(),
                is_deleted=False,
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class QuestionCreateView(auth_mixins.LoginRequiredMixin, generic.CreateView):
    template_name = 'questions/form.html'


class QuestionUpdateView(auth_mixins.LoginRequiredMixin, generic.UpdateView):
    template_name = 'questions/form.html'


class QuestionDetailView(auth_mixins.LoginRequiredMixin, generic.DetailView):
    template_name = 'questions/detail.html'


class QuestionDeleteView(auth_mixins.LoginRequiredMixin, generic.DeleteView):
    template_name = 'questions/delete.html'
