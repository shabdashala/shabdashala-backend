from django.urls import path
from . import views as home_views

app_name = 'home'

urlpatterns = [
    path('', home_views.IndexView.as_view(), name='index'),
    path('about-us/', home_views.AboutUsView.as_view(), name='about-us'),
]
