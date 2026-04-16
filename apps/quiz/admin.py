from django.contrib import admin

from .models import Choice, Question, QuizResult


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4
    fields = ("key", "label", "text", "weights")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("order", "text", "weight")
    ordering = ("order",)
    inlines = [ChoiceInline]


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ("user", "primary_type", "secondary_type", "created_at")
    raw_id_fields = ("user", "primary_type", "secondary_type")
