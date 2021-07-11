import csv

from django.contrib import admin
from django.http import HttpResponse

from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from treebeard.admin import TreeAdmin


class ModelAdminActionsMixin(object):

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class ExportCsvMixin(object):

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(
            meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


class BaseModelAdmin(ModelAdminActionsMixin, admin.ModelAdmin):
    pass


class BaseImportExportModelAdmin(ModelAdminActionsMixin, ImportExportModelAdmin):
    pass


class BaseSimpleHistoryAdmin(ModelAdminActionsMixin, SimpleHistoryAdmin):
    pass


class BaseSimpleHistoryImportExportModelAdmin(ModelAdminActionsMixin, ImportExportModelAdmin):
    pass


class BaseTreeAdmin(ModelAdminActionsMixin, TreeAdmin):
    pass
