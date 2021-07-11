from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from rangefilter.filters import DateRangeFilter

from apps.core.base_admin import BaseImportExportModelAdmin, BaseModelAdmin

from . import filters as accounts_filters
from . import forms as accounts_forms
from . import models as accounts_models
from . import resources as accounts_resources

admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    ordering = ('name', )
    filter_horizontal = ('permissions', )

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == 'permissions':
            qs = kwargs.get('queryset', db_field.remote_field.model.objects)
            # Avoid a major performance hit resolving permission names which
            # triggers a content_type load:
            kwargs['queryset'] = qs.select_related('content_type')
        return super().formfield_for_manytomany(db_field, request=request, **kwargs)


@admin.register(accounts_models.User)
class UserAdmin(BaseModelAdmin, DjangoUserAdmin, BaseImportExportModelAdmin):
    resource_class = accounts_resources.UserResource
    add_form = accounts_forms.UserCreationForm
    fieldsets = (
        (None, {
            'fields': ['email', "password"]
        }),
        (_('Personal info'), {
            'fields': ['first_name', 'last_name', 'gender', 'mobile'],
        }),
        (_('Permissions'), {
            'fields': ['is_active', 'is_staff', 'is_superuser']
        }),
        (_('Important dates'), {
            'fields': ['last_login', 'date_joined']
        }),
    )
    readonly_fields = (
        'is_active', 'is_staff', 'is_superuser',
        'last_login', 'date_joined',
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    list_filter = (
        ('date_joined', DateRangeFilter, ),
        'is_staff',
        'is_superuser',
        'is_active',
        accounts_filters.GroupListFilter,
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'mobile')
    ordering = ('email',)


@admin.register(accounts_models.DeviceToken)
class DeviceTokenAdmin(BaseModelAdmin):
    list_display = [
        'user', 'device_type', 'device_id',
        'date_added', 'date_removed', 'is_active'
    ]
    exclude = ['key']
    ordering = ['-date_added', '-date_removed']
    readonly_fields = [
        'user', 'device_type', 'device_id', 'date_added',
        'date_removed', 'is_active',
    ]
    list_filter = ['device_type', 'date_added', 'date_removed']
