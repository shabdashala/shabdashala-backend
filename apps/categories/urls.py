from django.urls import path
from . import views as categories_views

app_name = 'categories'

urlpatterns = [
    path('', categories_views.CategoriesIndexView.as_view(), name='index'),
    path('all/', categories_views.CategoriesListView.as_view(), name='list'),
    path('create/', categories_views.CategoriesCreateView.as_view(), name='create'),
    path('<slug:slug>-<int:pk>/', categories_views.CategoriesDetailView.as_view(), name='detail'),
    path('<slug:slug>-<int:pk>/edit/', categories_views.CategoriesUpdateView.as_view(), name='update'),
    path('<slug:slug>-<int:pk>/', categories_views.CategoriesDeleteView.as_view(), name='delete'),
]
