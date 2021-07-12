from django.contrib import admin
from django.urls import include, path, re_path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from allauth.account import views as allauth_views


schema_view = get_schema_view(
   openapi.Info(
      title="ShabdaShala API",
      default_version='v1',
      description="",
      terms_of_service="https://www.shabdashala.com/policies/terms/",
      contact=openapi.Contact(email="balu@shabdashala.com"),
      # license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # re_path('^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(
        r"^api/auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$",
        allauth_views.confirm_email,
        name="account_confirm_email",
    ),
    path('admin/', admin.site.urls),
    path('accounts/social', include('allauth.socialaccount.providers.facebook.urls')),
    path('accounts/social', include('allauth.socialaccount.urls')),
    path('accounts/', include('apps.accounts.urls.allauth')),
    path('api/auth/', include('apps.accounts.urls.api')),
]
