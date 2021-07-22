from django.urls import path
from . import views as quotes_views

app_name = 'quotes'

urlpatterns = [  # noqa
    path('', quotes_views.QuoteIndexView.as_view(), name='index'),
    path('all/', quotes_views.QuoteListView.as_view(), name='list'),
    path('create/', quotes_views.QuoteCreateView.as_view(), name='create'),
    path('<int:pk>/', quotes_views.QuoteDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', quotes_views.QuoteUpdateView.as_view(), name='update'),
    path('<int:pk>/', quotes_views.QuoteDetailView.as_view(), name='delete'),
]
