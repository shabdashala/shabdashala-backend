from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _


class GroupListFilter(admin.SimpleListFilter):

    title = _('groups')
    parameter_name = 'id'

    def lookups(self, request, model_admin):
        return Group.objects.order_by('name').values_list('id', 'name')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(groups__id__in=self.value())
        return queryset
