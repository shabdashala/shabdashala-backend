# Generated by Django 3.2.5 on 2021-07-26 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_attempts', '0004_auto_20210725_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizattempt',
            name='abandoned_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Abandoned Date and time?'),
        ),
        migrations.AddField(
            model_name='quizattempt',
            name='is_abandoned',
            field=models.BooleanField(default=False, verbose_name='Is Abandoned?'),
        ),
    ]
