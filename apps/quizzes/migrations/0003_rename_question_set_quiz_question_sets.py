# Generated by Django 3.2.5 on 2021-07-25 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0002_auto_20210725_1115'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quiz',
            old_name='question_set',
            new_name='question_sets',
        ),
    ]
