from django.contrib import admin

from treebeard.admin import TreeAdmin

from . import models as words_models


@admin.register(words_models.Word)
class WordAdmin(TreeAdmin):
    list_display = ('name', 'depth', 'display_order', 'is_active')
    readonly_fields = ['path', 'depth', 'numchild']
    list_editable = ['display_order', 'is_active']
    search_fields = ['name']
