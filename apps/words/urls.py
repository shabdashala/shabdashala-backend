from django.urls import path
from . import views as words_views

app_name = 'words'

urlpatterns = [
    path('', words_views.WordsIndexView.as_view(), name='index'),
    path('all/', words_views.WordsListView.as_view(), name='list'),
    path('create/', words_views.WordsCreateView.as_view(), name='create'),
    path('<slug:slug>-<int:pk>/', words_views.WordsDetailView.as_view(), name='detail'),
    path('<slug:slug>-<int:pk>/edit/', words_views.WordsUpdateView.as_view(), name='update'),
    path('<slug:slug>-<int:pk>/', words_views.WordsDeleteView.as_view(), name='delete'),
]
