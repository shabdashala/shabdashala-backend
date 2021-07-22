from django.urls import path
from . import views as languages_views

app_name = 'languages'

urlpatterns = [  # noqa
    path('', languages_views.LanguageIndexView.as_view(), name='index'),
    path('all/', languages_views.LanguageIndexView.as_view(), name='list'),
    path('create/', languages_views.LanguageCreateView.as_view(), name='create'),
    path('<slug:slug>-<int:pk>/', languages_views.LanguageDetailView.as_view(), name='detail'),
    path('<slug:slug>-<int:pk>/edit/', languages_views.LanguageDetailView.as_view(), name='update'),
    path('<slug:slug>-<int:pk>/', languages_views.LanguageDeleteView.as_view(), name='delete'),
]
