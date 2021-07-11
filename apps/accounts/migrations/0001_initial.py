# Generated by Django 3.2.5 on 2021-07-11 16:15

import apps.accounts.models
import apps.accounts.utils
from django.conf import settings
import django.contrib.postgres.fields.citext
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', django.contrib.postgres.fields.citext.CIEmailField(max_length=254, unique=True, verbose_name='email address')),
                ('mobile', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Phone number')),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=16, null=True, verbose_name='gender')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('force_password_reset', models.BooleanField(default=False, help_text='Designates whether this user should change his password during the next login.', verbose_name='password reset')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('image', models.ImageField(blank=True, null=True, upload_to=apps.accounts.utils.get_user_image_upload_path)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', apps.accounts.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='DeviceToken',
            fields=[
                ('device_type', models.CharField(blank=True, choices=[('ios', 'ios'), ('android', 'android'), ('web', 'web')], db_index=True, max_length=10, null=True)),
                ('device_id', models.CharField(blank=True, db_index=True, help_text='Unique device identifier', max_length=150, null=True, verbose_name='Device ID')),
                ('key', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='Key')),
                ('is_active', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(blank=True, null=True, verbose_name='Date Created')),
                ('date_removed', models.DateTimeField(blank=True, null=True, verbose_name='Date Removed')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devices', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'device token',
                'verbose_name_plural': 'device tokens',
            },
        ),
    ]
