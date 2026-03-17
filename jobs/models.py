from django.db import models


class JobMajor(models.Model):
    """
    Simple lookup table tying jobs to the same major keys used across the site
    (career quiz, resumes, colleges).
    """

    key = models.CharField(
        max_length=64,
        unique=True,
        help_text="Internal major key used elsewhere in the site, for example: computer_science, business, engineering.",
    )
    label = models.CharField(
        max_length=128,
        help_text='Human-friendly name shown to students, for example: "Computer Science & IT" or "Business & Management".',
    )

    class Meta:
        verbose_name = "Job major"
        verbose_name_plural = "Job majors"

    def __str__(self) -> str:
        return self.label


class Job(models.Model):
    """
    Job or internship opportunity surfaced to students.
    """

    EMPLOYMENT_TYPE_INTERNSHIP = "internship"
    EMPLOYMENT_TYPE_FULL_TIME = "full_time"
    EMPLOYMENT_TYPE_PART_TIME = "part_time"
    EMPLOYMENT_TYPE_CHOICES = [
        (EMPLOYMENT_TYPE_INTERNSHIP, "Internship"),
        (EMPLOYMENT_TYPE_FULL_TIME, "Full-time"),
        (EMPLOYMENT_TYPE_PART_TIME, "Part-time"),
    ]

    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(
        max_length=2,
        blank=True,
        help_text="Two-letter US state code (e.g. CA, NY). Leave blank for remote-only roles.",
    )
    is_remote = models.BooleanField(default=False)
    employment_type = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default=EMPLOYMENT_TYPE_INTERNSHIP,
    )
    majors = models.ManyToManyField(
        JobMajor,
        related_name="jobs",
        help_text="Which majors is this role most relevant for?",
    )
    url = models.URLField(
        max_length=500,
        help_text="Link to the external job posting or application page.",
    )
    description = models.TextField(
        help_text="Short, student-friendly summary shown in the listings."
    )
    posted_at = models.DateField(
        null=True,
        blank=True,
        help_text="Optional posted date for display and ordering.",
    )
    source = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional source label (e.g. 'Company career site', 'Example data').",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to hide this job from the public listings without deleting it.",
    )

    class Meta:
        ordering = ["-posted_at", "-created_at"]

    def __str__(self) -> str:
        return f"{self.title} at {self.company}"

