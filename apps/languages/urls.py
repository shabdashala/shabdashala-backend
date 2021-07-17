from django.urls import path
from . import views as languages_views

app_name = 'languages'

urlpatterns = [
    path('', languages_views.LanguagesIndexView.as_view(), name='index'),
    path('all/', languages_views.LanguagesIndexView.as_view(), name='list'),
    path('create/', languages_views.LanguagesCreateView.as_view(), name='create'),
    path('<slug:slug>-<int:pk>/', languages_views.LanguagesDetailView.as_view(), name='detail'),
    path('<slug:slug>-<int:pk>/edit/', languages_views.LanguagesDetailView.as_view(), name='update'),
    path('<slug:slug>-<int:pk>/', languages_views.LanguagesDeleteView.as_view(), name='delete'),
]
