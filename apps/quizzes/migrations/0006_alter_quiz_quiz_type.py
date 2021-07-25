# Generated by Django 3.2.5 on 2021-07-25 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0005_auto_20210725_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='quiz_type',
            field=models.CharField(choices=[('adaptive', 'Adaptive'), ('configured', 'నిర్దిష్టమయిన'), ('dynamic', 'క్రియాశీలక')], db_index=True, default='dynamic', max_length=16, verbose_name='ప్రశ్నల పరీక్ష రకం'),
        ),
    ]
