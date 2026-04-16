from django.contrib import admin

from .models import Job, Major, PersonalityType


@admin.register(PersonalityType)
class PersonalityTypeAdmin(admin.ModelAdmin):
    list_display = ("key", "name", "icon")
    search_fields = ("key", "name")


@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    list_display = ("key", "name")
    search_fields = ("key", "name")
    filter_horizontal = ("personality_types",)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "primary_archetype")
    search_fields = ("title",)
    list_filter = ("primary_archetype",)
    filter_horizontal = ("majors",)
    raw_id_fields = ("primary_archetype",)
