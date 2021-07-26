# Generated by Django 3.2.5 on 2021-07-26 21:23

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_attempts', '0005_auto_20210726_2028'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizattempt',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
