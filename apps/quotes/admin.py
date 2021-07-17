from django.contrib import admin
from apps.core.base_admin import BaseModelAdmin

from . import models as riddles_models


@admin.register(riddles_models.Quote)
class QuoteAdmin(BaseModelAdmin):
    list_display = ['language', 'text', 'is_active', 'created', 'modified']
    ordering = ['language', 'is_active']
