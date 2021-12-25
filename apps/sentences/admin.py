from django.contrib import admin
from apps.core.base_admin import BaseModelAdmin

from . import models as sentences_models


class SentenceTranslationInline(admin.TabularInline):
    model = sentences_models.SentenceTranslation
    # To fix (admin.E202):
    # 'sentences.SentenceTranslation' has more than one ForeignKey to 'sentences.Sentence'.
    # You must specify a 'fk_name' attribute.
    fk_name = 'sentence'


@admin.register(sentences_models.Sentence)
class SentenceAdmin(BaseModelAdmin):
    list_display = ['id', 'language', 'text', 'is_active', 'is_deleted', 'date_removed']
    ordering = ['language', 'is_active']
    inlines = [SentenceTranslationInline]
