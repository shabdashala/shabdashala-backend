from django.contrib import admin

from . import models as quizzes_models


@admin.register(quizzes_models.Quiz)
class QuizAdmin(admin.ModelAdmin):
    pass
