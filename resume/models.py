from django.db import models
from django.conf import settings


class SavedDocument(models.Model):
    DOC_TYPE_CHOICES = [
        ('resume', 'Resume'),
        ('cover_letter', 'Cover letter'),
        ('admissions_essay', 'Admissions essay'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saved_documents',
    )
    title = models.CharField(max_length=200)
    major_key = models.CharField(max_length=80, blank=True, null=True)
    doc_type = models.CharField(max_length=20, choices=DOC_TYPE_CHOICES, default='resume')
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.title} ({self.get_doc_type_display()})"
