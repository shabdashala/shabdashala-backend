from rest_framework import serializers

from apps.accounts import models as accounts_models


class UserDetailsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    gender = serializers.ChoiceField(
        required=True,
        choices=accounts_models.User.GENDER_CHOICES)

    class Meta:
        model = accounts_models.User
        fields = [
            'id', 'email', 'mobile',
            'first_name', 'last_name',
            'image', 'gender',
        ]
        read_only_fields = ['id', 'email']

    def get_image(self, instance):
        return instance.image_url


__all__ = [
    'UserDetailsSerializer',
]
