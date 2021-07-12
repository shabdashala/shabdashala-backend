from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView,
)
from .. import views as accounts_views

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('facebook/', accounts_views.FacebookLogin.as_view(), name='fb_login'),
    path('', include('dj_rest_auth.urls')),
]
