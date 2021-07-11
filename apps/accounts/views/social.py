from allauth.socialaccount.providers.facebook import views as facebook_views
from allauth.socialaccount.providers.github import views as github_views
from allauth.socialaccount.providers.google import views as google_views
from allauth.socialaccount.providers.instagram import views as instagram_views
from allauth.socialaccount.providers.linkedin_oauth2 import \
    views as linkedin_views
from allauth.socialaccount.providers.twitter import views as twitter_views

from dj_rest_auth.registration.views import SocialLoginView


class FacebookLogin(SocialLoginView):
    adapter_class = facebook_views.FacebookOAuth2Adapter


class TwitterLogin(SocialLoginView):
    adapter_class = twitter_views.TwitterOAuthAdapter


class GitHubLogin(SocialLoginView):
    adapter_class = github_views.GitHubOAuth2Adapter


class GoogleLogin(SocialLoginView):
    adapter_class = google_views.GoogleOAuth2Adapter


class InstagramLogin(SocialLoginView):
    adapter_class = instagram_views.InstagramOAuth2Adapter


class LinkedInLogin(SocialLoginView):
    adapter_class = linkedin_views.LinkedInOAuth2Adapter
