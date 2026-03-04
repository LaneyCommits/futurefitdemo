"""Chat threads and messages for the chatbot."""
from django.conf import settings
from django.db import models


class ChatThread(models.Model):
    """One thread per user (single ongoing conversation)."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chat_thread',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ChatThread({self.user.username})"


class ChatMessage(models.Model):
    """A single message in a thread."""
    ROLE_USER = 'user'
    ROLE_ASSISTANT = 'assistant'

    thread = models.ForeignKey(
        ChatThread,
        on_delete=models.CASCADE,
        related_name='messages',
    )
    role = models.CharField(max_length=16, choices=[(ROLE_USER, 'User'), (ROLE_ASSISTANT, 'Assistant')])
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."
