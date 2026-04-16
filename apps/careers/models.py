from django.db import models


class PersonalityType(models.Model):
    key = models.SlugField(max_length=64, unique=True)
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    traits = models.JSONField(
        default=list,
        blank=True,
        help_text="List of trait strings, e.g. ['analytical', 'methodical'].",
    )
    icon = models.CharField(max_length=8, blank=True)
    career_direction = models.TextField(
        blank=True,
        help_text="Short prose on the career direction for this archetype.",
    )
    strengths = models.TextField(blank=True)
    growth_areas = models.TextField(
        blank=True,
        help_text="Subtle growth areas (not weaknesses).",
    )
    identity_statement = models.TextField(
        blank=True,
        help_text="First-person identity statement used in results.",
    )
    behavioral_explanation = models.TextField(
        blank=True,
        help_text="Paragraph explaining thinking style.",
    )
    why_this_fits = models.TextField(
        blank=True,
        help_text="Paragraph on why this archetype fits the user.",
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Major(models.Model):
    key = models.SlugField(max_length=64, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    personality_types = models.ManyToManyField(
        PersonalityType,
        related_name="majors",
        blank=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    learn_more = models.TextField(blank=True)
    primary_archetype = models.ForeignKey(
        PersonalityType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="jobs",
    )
    majors = models.ManyToManyField(Major, related_name="jobs", blank=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title
