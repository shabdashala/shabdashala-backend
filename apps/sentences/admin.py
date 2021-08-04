from django.contrib import admin
from apps.core.base_admin import BaseModelAdmin

from . import models as sentences_models


@admin.register(sentences_models.Sentence)
class SentenceAdmin(BaseModelAdmin):
    list_display = ['id', 'language', 'text', 'is_active', 'is_deleted', 'date_removed']
    ordering = ['language', 'is_active']
