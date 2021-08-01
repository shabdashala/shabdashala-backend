from django.contrib import admin

from . import models as quiz_attempts_models


class AttemptedQuestionInline(admin.StackedInline):
    model = quiz_attempts_models.AttemptedQuestion
    extra = 0


@admin.register(quiz_attempts_models.QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    inlines = [AttemptedQuestionInline]
    list_display = ['uuid', 'quiz']
