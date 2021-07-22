from django.urls import path
from . import views as words_views

app_name = 'words'

urlpatterns = [  # noqa
    path('', words_views.WordIndexView.as_view(), name='index'),
    path('all/', words_views.WordListView.as_view(), name='list'),
    path('create/', words_views.WordCreateView.as_view(), name='create'),
    path('<slug:slug>-<int:pk>/', words_views.WordDetailView.as_view(), name='detail'),
    path('<slug:slug>-<int:pk>/edit/', words_views.WordUpdateView.as_view(), name='update'),
    path('<slug:slug>-<int:pk>/', words_views.WordDeleteView.as_view(), name='delete'),
]
