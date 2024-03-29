from importlib import import_module

from django.urls import include, path, re_path, reverse_lazy
from django.views.generic import RedirectView

from allauth import app_settings
from allauth.account import views as allauth_views
from allauth.socialaccount import providers

urlpatterns = [
    path("register/", RedirectView.as_view(url=reverse_lazy('account_signup')), name="account_register"),
    path("signin/", RedirectView.as_view(url=reverse_lazy('account_login')), name="account_signin"),

    path("signup/", allauth_views.signup, name="account_signup"),
    path("login/", allauth_views.login, name="account_login"),
    path("logout/", allauth_views.logout, name="account_logout"),
    path(
        "password/change/",
        allauth_views.password_change,
        name="account_change_password",
    ),
    path("password/set/", allauth_views.password_set, name="account_set_password"),
    path("inactive/", allauth_views.account_inactive, name="account_inactive"),
    # E-mail
    path("email/", allauth_views.email, name="account_email"),
    path(
        "confirm-email/",
        allauth_views.email_verification_sent,
        name="account_email_verification_sent",
    ),
    re_path(
        r"^confirm-email/(?P<key>[-:\w]+)/$",
        allauth_views.confirm_email,
        name="account_confirm_email",
    ),
    # password reset
    path("password/reset/", allauth_views.password_reset, name="account_reset_password"),
    path(
        "password/reset/done/",
        allauth_views.password_reset_done,
        name="account_reset_password_done",
    ),
    re_path(
        r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        allauth_views.password_reset_from_key,
        name="account_reset_password_from_key",
    ),
    path(
        "password/reset/key/done/",
        allauth_views.password_reset_from_key_done,
        name="account_reset_password_from_key_done",
    ),
]

if app_settings.SOCIALACCOUNT_ENABLED:
    urlpatterns += [re_path(r'^social/', include('allauth.socialaccount.urls'))]

for provider in providers.registry.get_list():
    try:
        prov_mod = import_module(provider.get_package() + '.urls')
    except ImportError:
        continue
    prov_urlpatterns = getattr(prov_mod, 'urlpatterns', None)
    if prov_urlpatterns:
        urlpatterns += prov_urlpatterns
