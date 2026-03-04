"""Profile and email verification."""
import secrets
from django.conf import settings
from django.db import models


class Profile(models.Model):
    """One-to-one profile: verification, avatar, bio, AI personalization."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    email_verified = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/%Y/%m/', blank=True, null=True)
    bio = models.TextField(blank=True)
    # AI personalization (for chatbot and AI tools)
    custom_instructions = models.TextField(
        blank=True,
        help_text='How you want the AI to respond (e.g. tone, style).',
    )
    BASE_STYLE_CHOICES = [
        ('', 'Default'),
        ('friendly', 'Friendly'),
        ('professional', 'Professional'),
        ('concise', 'Concise'),
        ('detailed', 'Detailed'),
    ]
    base_style = models.CharField(
        max_length=32,
        choices=BASE_STYLE_CHOICES,
        default='',
        blank=True,
    )
    # Optional toggles stored as JSON: e.g. {"warm": true, "enthusiastic": true, "use_headers": true, "use_emoji": false}
    ai_toggles = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Profile({self.user.username})"


class EmailVerification(models.Model):
    """One-time token sent to user's email for verification."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='email_verifications',
    )
    key = models.CharField(max_length=64, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @classmethod
    def create_for_user(cls, user):
        key = secrets.token_urlsafe(32)
        return cls.objects.create(user=user, key=key)

    def __str__(self):
        return f"EmailVerification({self.user.username})"
