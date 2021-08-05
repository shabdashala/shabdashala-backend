from django.urls import path

from apps.questions import views as questions_views
from . import views as categories_views

app_name = 'categories'

urlpatterns = [  # noqa
    path('', categories_views.CategoryIndexView.as_view(), name='index'),
    path('all/', categories_views.CategoryListView.as_view(), name='list'),
    path('create/', categories_views.CategoryCreateView.as_view(), name='create'),
    path('<str:slug>-<int:pk>/', categories_views.CategoryDetailView.as_view(), name='detail'),
    path('<str:slug>-<int:pk>/edit/', categories_views.CategoryUpdateView.as_view(), name='update'),
    path('<str:slug>-<int:pk>/', categories_views.CategoryDeleteView.as_view(), name='delete'),

    path('<str:category_slug>-<int:category_pk>/questions/', questions_views.QuestionListView.as_view(),
         name='categories-questions'),
]
