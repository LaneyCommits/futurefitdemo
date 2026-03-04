from django.conf import settings
from django.db import models


class QuizResult(models.Model):
    """Latest quiz results per user for display on profile (e.g. as pills)."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='quiz_result',
    )
    # Labels to show as pills: top category names and/or top career titles
    pill_labels = models.JSONField(
        default=list,
        help_text='List of strings, e.g. top category names and career titles.',
    )
    is_explore = models.BooleanField(
        default=False,
        help_text='True if from explore quiz (no major).',
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"QuizResult({self.user.username})"
