from django.contrib import admin

from .models import Job, JobMajor


@admin.register(JobMajor)
class JobMajorAdmin(admin.ModelAdmin):
    list_display = ("label", "key")
    search_fields = ("label", "key")


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "employment_type", "state", "is_remote", "is_active")
    list_filter = ("employment_type", "is_remote", "state", "is_active", "majors")
    search_fields = ("title", "company", "description")
    filter_horizontal = ("majors",)
    autocomplete_fields = ()
    fieldsets = (
        (
            "Job info",
            {
                "fields": (
                    "title",
                    "company",
                    "employment_type",
                    "majors",
                    "is_active",
                )
            },
        ),
        (
            "Location",
            {
                "fields": (
                    "city",
                    "state",
                    "is_remote",
                )
            },
        ),
        (
            "Listing",
            {
                "fields": (
                    "url",
                    "description",
                    "posted_at",
                    "source",
                )
            },
        ),
    )

