from django.contrib import admin

from treebeard.admin import TreeAdmin

from . import models as categories_models


@admin.register(categories_models.Category)
class CategoryAdmin(TreeAdmin):
    list_display = ['name', 'slug', 'display_order', 'is_active', 'is_deleted', 'date_removed']
    list_editable = ['display_order', 'is_active']
    search_fields = ['name']
