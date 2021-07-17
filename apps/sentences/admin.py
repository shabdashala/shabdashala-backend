from django.contrib import admin
from apps.core.base_admin import BaseModelAdmin

from . import models as sentences_models


@admin.register(sentences_models.Sentence)
class SentenceAdmin(BaseModelAdmin):
    list_display = ['language', 'text', 'is_active']
    ordering = ['language', 'is_active']
