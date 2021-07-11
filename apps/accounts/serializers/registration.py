from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.utils import email_address_exists
from rest_framework import serializers


class RegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)

    email = serializers.EmailField(required=settings.ACCOUNT_UNIQUE_EMAIL)
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    device_id = serializers.CharField(required=False, allow_blank=True)
    device_type = serializers.CharField(required=False, allow_blank=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if settings.ACCOUNT_UNIQUE_EMAIL:
            if email and email_address_exists(email):
                msg = "A user is already registered with this e-mail address."
                raise serializers.ValidationError(_(msg))
        return email

    def validate_password(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError(
                _("The two password fields didn't match.")
            )
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'email': self.validated_data.get('email', ''),
            'password': self.validated_data.get('password', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user
