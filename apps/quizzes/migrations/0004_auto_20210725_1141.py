# Generated by Django 3.2.5 on 2021-07-25 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0003_rename_question_set_quiz_question_sets'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizquestion',
            name='display_order',
            field=models.PositiveIntegerField(default=0, verbose_name='ప్రదర్శన క్రమం'),
        ),
        migrations.AlterField(
            model_name='quizquestionset',
            name='display_order',
            field=models.PositiveIntegerField(default=0, verbose_name='ప్రదర్శన క్రమం'),
        ),
    ]
