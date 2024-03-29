# Generated by Django 3.2.5 on 2021-07-25 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_auto_20210724_1927'),
        ('questions', '0002_auto_20210724_2137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionset',
            name='question',
        ),
        migrations.AddField(
            model_name='questionset',
            name='categories',
            field=models.ManyToManyField(blank=True, to='categories.Category'),
        ),
        migrations.AlterField(
            model_name='questionset',
            name='display_order',
            field=models.PositiveIntegerField(default=0, verbose_name='ప్రదర్శన క్రమం'),
        ),
    ]
