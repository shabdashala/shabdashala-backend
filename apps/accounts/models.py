"""Accounts related models."""
import binascii
import os
import uuid

from django.contrib.auth import models as django_auth_models
from django.core.mail import send_mail
from django.db import models
from django.contrib.postgres.fields import CIEmailField
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from . import utils as accounts_utils


class UserManager(django_auth_models.BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.username = email
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(django_auth_models.AbstractBaseUser, django_auth_models.PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions.

    Email and password are required. Other fields are optional.
    """
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'

    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    )

    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4,
        editable=False, db_index=True)

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = CIEmailField(_('email address'), unique=True)
    mobile = PhoneNumberField(_("Phone number"), blank=True, null=True)
    gender = models.CharField(
        _('gender'),
        max_length=16,
        blank=True, null=True,
        choices=GENDER_CHOICES)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ))
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ))

    force_password_reset = models.BooleanField(
        _('password reset'),
        default=False,
        help_text=_(
            'Designates whether this user should change his password '
            'during the next login.'
        ))

    date_joined = models.DateTimeField(
        _('date joined'), default=timezone.now)
    image = models.ImageField(
        null=True, blank=True,
        upload_to=accounts_utils.get_user_image_upload_path)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    # def delete(self, **kwargs):
    #     self.is_active = False
    #     self.save()

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_display_name(self):
        return self.get_full_name() or self.email

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Returns the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def set_password(self, raw_password):
        super().set_password(raw_password)
        self.force_password_reset = False

    @property
    def image_url(self):
        return self.image.url if self.image and self.image.url else ''


class DeviceToken(models.Model):
    DEVICE_IOS = 'ios'
    DEVICE_ANDROID = 'android'
    DEVICE_WEB = 'web'
    DEVICE_TYPES = (
        (DEVICE_IOS, 'ios'),
        (DEVICE_ANDROID, 'android'),
        (DEVICE_WEB, 'web'))

    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='devices')

    device_type = models.CharField(
        choices=DEVICE_TYPES, max_length=10,
        null=True, blank=True, db_index=True)
    device_id = models.CharField(
        verbose_name=_("Device ID"), db_index=True,
        help_text=_("Unique device identifier"),
        max_length=150, null=True, blank=True)

    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    is_active = models.BooleanField(default=True)

    date_added = models.DateTimeField(
        _("Date Created"), null=True, blank=True)
    date_removed = models.DateTimeField(
        _("Date Removed"), null=True, blank=True)

    def __str__(self):
        full_name = self.user.get_full_name()
        user = full_name if full_name else self.user.email
        return "user: {user} - device_type: {device_type}" \
            " - device_id: {device_id}".format(
                user=user, device_type=self.device_type,
                device_id=self.device_id)

    class Meta:
        verbose_name = _('device token')
        verbose_name_plural = _('device tokens')

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def delete(self, **kwargs):
        self.is_active = False
        self.date_removed = timezone.now()
        self.save()
