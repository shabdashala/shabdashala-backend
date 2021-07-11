from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from allauth.account.utils import send_email_confirmation
from dj_rest_auth import serializers as dj_rest_auth_serializers
from rest_framework import exceptions, serializers

from apps.accounts import models as accounts_models


class LoginSerializer(dj_rest_auth_serializers.LoginSerializer):

    device_id = serializers.CharField(required=False, allow_blank=True)
    device_type = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if not (email and password):
            msg = _("Invalid credentials!")
            raise exceptions.ValidationError(msg)

        email = email.lower()
        try:
            user_instance = accounts_models.User.objects.get(email__iexact=email)
            if user_instance.force_password_reset:
                msg = _('Please reset your password to access your account.')
                raise exceptions.ValidationError(msg)
        except accounts_models.User.DoesNotExist:
            msg = _("This email address hasn't been registered with us.")
            raise exceptions.ValidationError(msg)

        user = self._validate_email(email, password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        elif user_instance and user_instance.is_active:
            msg = _('Incorrect Password. Please try again!')
            raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        # If required, is the email verified?
        if 'rest_auth.registration' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            if app_settings.EMAIL_VERIFICATION == \
                    app_settings.EmailVerificationMethod.MANDATORY:
                verified_email_addresses = user.emailaddress_set.filter(
                    email=user.email, verified=True)
                if not verified_email_addresses.exists():
                    send_email_confirmation(
                        self.context['request'], user, False)
                    msg = _("Your E-mail address is not verified. "
                            "A verification e-mail is sent to your inbox.")
                    raise serializers.ValidationError(msg)
        attrs['user'] = user
        return attrs


__all__ = [
    'LoginSerializer'
]
