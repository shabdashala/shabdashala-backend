# Generated by Django 3.2.5 on 2021-07-17 00:05

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
        ('languages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, unique=True)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('name', models.CharField(db_index=True, max_length=255, verbose_name='Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('meta_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Meta title')),
                ('meta_description', models.TextField(blank=True, null=True, verbose_name='Meta description')),
                ('image', models.ImageField(blank=True, max_length=255, null=True, upload_to='categories', verbose_name='Image')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, max_length=255, populate_from='name', verbose_name='Slug')),
                ('is_public', models.BooleanField(db_index=True, default=True, help_text='Show this category in search results and word listings.', verbose_name='Is public')),
                ('ancestors_are_public', models.BooleanField(db_index=True, default=True, help_text='The ancestors of this word are public', verbose_name='Ancestor words are public')),
                ('display_order', models.PositiveIntegerField(verbose_name='Display order')),
                ('is_active', models.BooleanField(default=False)),
                ('categories', models.ManyToManyField(blank=True, to='categories.Category')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='languages.language')),
                ('translations', models.ManyToManyField(blank=True, related_name='_words_word_translations_+', to='words.Word')),
            ],
            options={
                'verbose_name': 'Word',
                'verbose_name_plural': 'Words',
                'ordering': ['path'],
            },
        ),
    ]