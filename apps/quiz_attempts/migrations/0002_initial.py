# Generated by Django 3.2.5 on 2021-07-24 17:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('quizzes', '0001_initial'),
        ('questions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz_attempts', '0001_initial'),
        ('sentences', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizattempt',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzes.quiz', verbose_name='ప్రశ్నల పరీక్ష'),
        ),
        migrations.AddField(
            model_name='quizattempt',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='వినియోగదారు'),
        ),
        migrations.AddField(
            model_name='attemptedquestion',
            name='entered_text',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sentences.sentence', verbose_name='Sentence'),
        ),
        migrations.AddField(
            model_name='attemptedquestion',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.question'),
        ),
        migrations.AddField(
            model_name='attemptedquestion',
            name='quiz_attempt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempted_questions', to='quiz_attempts.quizattempt'),
        ),
        migrations.AddField(
            model_name='attemptedquestion',
            name='selected_choice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='questions.choice'),
        ),
        migrations.AddField(
            model_name='attemptedquestion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='వినియోగదారు'),
        ),
    ]
