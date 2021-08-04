from django.contrib import admin
from apps.core.base_admin import BaseModelAdmin

from . import models as languages_models


@admin.register(languages_models.Language)
class LanguageAdmin(BaseModelAdmin):
    list_display = [
        'name', 'english_name', 'two_letter_code',
        'three_letter_code', 'display_order', 'is_active',
        'is_deleted', 'date_removed',
    ]
    ordering = ['english_name', '-display_order']
