from django.urls import path
from . import views as sentences_views

app_name = 'sentences'

urlpatterns = [
    path('', sentences_views.SentencesIndexView.as_view(), name='index'),
    path('all/', sentences_views.SentencesListView.as_view(), name='list'),
    path('create/', sentences_views.SentencesCreateView.as_view(), name='create'),
    path('<int:pk>/', sentences_views.SentencesDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', sentences_views.SentencesUpdateView.as_view(), name='update'),
    path('<int:pk>/', sentences_views.SentencesDeleteView.as_view(), name='delete'),
]
