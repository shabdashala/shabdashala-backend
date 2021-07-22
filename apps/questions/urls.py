from django.urls import path
from . import views as questions_views

app_name = 'questions'

urlpatterns = [  # noqa
    path('', questions_views.QuestionIndexView.as_view(), name='index'),
    path('all/', questions_views.QuestionListView.as_view(), name='list'),
    path('create/', questions_views.QuestionCreateView.as_view(), name='create'),
    path('<int:pk>/', questions_views.QuestionDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', questions_views.QuestionUpdateView.as_view(), name='update'),
    path('<int:pk>/', questions_views.QuestionDeleteView.as_view(), name='delete'),
]
