from django.utils import timezone

EXCLUDED_VALUES = ['', 'null', 'undefined']


def get_user_image_upload_path(instance, file_name):
    file_ext = file_name.split(".")[-1]
    return "{}/{}/{}.{}".format(
        instance._meta.app_label,
        instance._meta.model_name,
        str(instance.uuid),
        file_ext).lower()


def create_device_token(token_model, user, serializer):
    device_type = serializer.data.get('device_type')
    device_id = serializer.data.get('device_id')

    if device_type in EXCLUDED_VALUES:
        device_type = None
    if device_id in EXCLUDED_VALUES:
        device_id = None

    # If there are existing tokens for the given device, then mark them removed
    existing_tokens = token_model.objects.filter(
        device_id=device_id, is_active=True)
    if not device_id:
        existing_tokens = existing_tokens.filter(user=user)

    existing_tokens.update(date_removed=timezone.now(), is_active=False)
    return token_model.objects.create(
        user=user, device_type=device_type,
        device_id=device_id,
        date_added=timezone.now())
