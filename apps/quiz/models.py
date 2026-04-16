from django.conf import settings
from django.db import models


class Question(models.Model):
    text = models.TextField()
    order = models.PositiveIntegerField(default=0, db_index=True)
    weight = models.FloatField(
        default=1.0,
        help_text="Scoring multiplier for this question (1.0, 1.5, or 2.0).",
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Q{self.order}: {self.text[:60]}"


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choices"
    )
    key = models.CharField(
        max_length=16,
        help_text="Unique option key submitted by the frontend (e.g. q1a).",
    )
    label = models.CharField(
        max_length=1,
        default="A",
        help_text="Display label: A, B, C, or D.",
    )
    text = models.CharField(max_length=255)
    weights = models.JSONField(
        default=dict,
        help_text=(
            "Per-archetype scoring weights for this choice. "
            'E.g. {"systems_thinker": 1.0, "analytical_solver": 0.4, ...}'
        ),
    )

    class Meta:
        ordering = ["question", "key"]

    def __str__(self):
        return f"{self.key}: {self.text[:50]}"


class QuizResult(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="quiz_results",
        null=True,
        blank=True,
    )
    primary_type = models.ForeignKey(
        "careers.PersonalityType",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="quiz_results_primary",
    )
    secondary_type = models.ForeignKey(
        "careers.PersonalityType",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="quiz_results_secondary",
    )
    answers = models.JSONField(
        default=dict,
        help_text="Raw submitted answers: {question_order: choice_key}.",
    )
    scores = models.JSONField(
        default=dict,
        help_text="Final archetype scores: {'systems_thinker': 8.5, ...}.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        user_label = self.user.username if self.user else "anonymous"
        return f"QuizResult({user_label}, {self.created_at:%Y-%m-%d})"
