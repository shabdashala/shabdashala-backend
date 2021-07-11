from rest_framework import serializers

from apps.accounts import models as accounts_models
from .user import UserDetailsSerializer


class TokenSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer()

    class Meta:
        model = accounts_models.DeviceToken
        fields = ['key', 'user']
        read_only_fields = ['key']


__all__ = [
    'TokenSerializer',
]
