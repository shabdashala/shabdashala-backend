# Generated by Django 3.2.5 on 2021-08-04 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_question_maximum_number_of_choices'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='date_removed',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='choice',
            name='is_deleted',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Is Deleted?'),
        ),
        migrations.AddField(
            model_name='question',
            name='date_removed',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='is_deleted',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Is Deleted?'),
        ),
        migrations.AddField(
            model_name='questionset',
            name='date_removed',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='questionset',
            name='is_deleted',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Is Deleted?'),
        ),
    ]
