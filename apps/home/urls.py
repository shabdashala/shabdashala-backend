from django.urls import path
from . import views as home_views

app_name = 'home'

urlpatterns = [
    path('', home_views.IndexView.as_view(), name='index'),
    path('about-us/', home_views.AboutUsView.as_view(), name='about-us'),
    path('practice/<uuid:quiz_uuid>/', home_views.PracticeStartView.as_view(), name='practice-start'),
    path('practice/<uuid:quiz_uuid>/<uuid:quiz_attemmpt_uuid>', home_views.PracticeProgressView.as_view(),
         name='practice-home'),
]
