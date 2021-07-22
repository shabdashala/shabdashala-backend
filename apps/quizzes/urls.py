from django.urls import include, path
from . import views as quiz_views

app_name = 'quizzes'

questions_urlpatterns = [
    path('create/', quiz_views.QuizQuestionCreateView.as_view(), name='create'),
    path('<int:pk>/', quiz_views.QuizQuestionDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', quiz_views.QuizQuestionUpdateView.as_view(), name='update'),
    path('<int:pk>/', quiz_views.QuizQuestionDetailView.as_view(), name='delete'),
]

urlpatterns = [
    path('', quiz_views.QuizIndexView.as_view(), name='index'),
    path('all/', quiz_views.QuizListView.as_view(), name='list'),
    path('create/', quiz_views.QuizCreateView.as_view(), name='create'),
    path('<int:pk>/', quiz_views.QuizDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', quiz_views.QuizUpdateView.as_view(), name='update'),
    path('<int:pk>/', quiz_views.QuizDetailView.as_view(), name='delete'),
    path('<int:quiz_pk>/questions/', include((questions_urlpatterns, 'quiz-questions'), namespace='quiz-questions')),
]
