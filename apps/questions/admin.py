from django.contrib import admin

from . import models as questions_models


@admin.register(questions_models.Question)
class QuestionAdmin(admin.ModelAdmin):
    pass
