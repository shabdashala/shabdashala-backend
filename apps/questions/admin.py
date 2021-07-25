from django.contrib import admin

from . import models as questions_models


class ChoiceInline(admin.TabularInline):
    model = questions_models.Choice
    extra = 2


@admin.register(questions_models.Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
