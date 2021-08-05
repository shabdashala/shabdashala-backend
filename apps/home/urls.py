from django.urls import path
from . import views as home_views

app_name = 'home'

urlpatterns = [
    path('', home_views.IndexView.as_view(), name='index'),
    path('leaderboard/', home_views.LeaderBoardView.as_view(), name='leaderboard'),
    path('privacy/', home_views.PrivacyPolicyView.as_view(), name='privacy'),
    path('about-us/', home_views.AboutUsView.as_view(), name='about-us'),
    path('practice/<str:quiz_slug>-<uuid:quiz_uuid>/', home_views.PracticeStartView.as_view(), name='practice-start'),
    path('practice/<str:quiz_slug>-<uuid:quiz_uuid>/attempt-<uuid:quiz_attempt_uuid>/',
         home_views.PracticeProgressView.as_view(),
         name='practice-home'),
    path('practice/<str:quiz_slug>-<uuid:quiz_uuid>/attempt-<uuid:quiz_attempt_uuid>/results/',
         home_views.PracticeResultsView.as_view(),
         name='practice-results'),
]
