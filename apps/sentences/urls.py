from django.urls import path
from . import views as sentences_views

app_name = 'sentences'

urlpatterns = [  # noqa
    path('', sentences_views.SentenceIndexView.as_view(), name='index'),
    path('all/', sentences_views.SentenceListView.as_view(), name='list'),
    path('create/', sentences_views.SentenceCreateView.as_view(), name='create'),
    path('<int:pk>/', sentences_views.SentenceDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', sentences_views.SentenceUpdateView.as_view(), name='update'),
    path('<int:pk>/', sentences_views.SentenceDeleteView.as_view(), name='delete'),
]
