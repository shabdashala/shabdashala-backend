# Generated by Django 3.2.5 on 2021-07-25 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_auto_20210725_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='maximum_number_of_choices',
            field=models.PositiveIntegerField(default=4, verbose_name='Maximum number of choices'),
        ),
    ]
