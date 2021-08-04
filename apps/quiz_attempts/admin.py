from django.contrib import admin

from . import models as quiz_attempts_models


class AttemptedQuestionInline(admin.StackedInline):
    model = quiz_attempts_models.AttemptedQuestion
    extra = 0


@admin.register(quiz_attempts_models.QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    inlines = [AttemptedQuestionInline]
    list_display = ['quiz', 'user', 'is_completed', 'is_abandoned', 'is_deleted', 'date_removed']
    list_filter = ['completed_at', 'is_completed', 'is_deleted', 'is_abandoned']
