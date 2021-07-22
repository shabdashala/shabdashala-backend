from django.urls import path
from . import views as quiz_attempts_views

app_name = 'quiz_attempts'

urlpatterns = [  # noqa
    path('', quiz_attempts_views.QuizAttemptIndexView.as_view(), name='index'),
    path('all/', quiz_attempts_views.QuizAttemptListView.as_view(), name='list'),
    path('create/', quiz_attempts_views.QuizAttemptCreateView.as_view(), name='create'),
    path('<int:pk>/', quiz_attempts_views.QuizAttemptDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', quiz_attempts_views.QuizAttemptUpdateView.as_view(), name='update'),
    path('<int:pk>/', quiz_attempts_views.QuizAttemptDetailView.as_view(), name='delete'),
]
