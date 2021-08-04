from django.contrib import admin

from . import models as quizzes_models


@admin.register(quizzes_models.Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'slug', 'language', 'category',
        'is_active', 'is_deleted', 'date_removed',
    ]
