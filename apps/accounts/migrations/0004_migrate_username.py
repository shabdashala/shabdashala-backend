from django.db import migrations
from django.utils.crypto import get_random_string


def forwards_func(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    for instance in User.objects.iterator():
        if not instance.username:
            instance.username = f"user-{get_random_string(8)}"
            instance.save()


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_username'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
