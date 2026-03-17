import logging

from django.core.management.base import BaseCommand

from career_quiz.quiz_data import MAJORS

from jobs.example_jobs import EXAMPLE_JOBS
from jobs.models import Job, JobMajor


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Seed the database with example job majors and job listings for demos."

    def handle(self, *args, **options):
        # Ensure JobMajor rows exist for all quiz majors
        key_to_major = {}
        for key, label, *_ in MAJORS:
            major, _ = JobMajor.objects.get_or_create(
                key=key,
                defaults={"label": label},
            )
            key_to_major[key] = major

        created_count = 0
        for job_data in EXAMPLE_JOBS:
            title = job_data["title"]
            company = job_data["company"]
            url = job_data["url"]

            job, created = Job.objects.get_or_create(
                title=title,
                company=company,
                url=url,
                defaults={
                    "city": job_data.get("city", ""),
                    "state": job_data.get("state", ""),
                    "is_remote": job_data.get("is_remote", False),
                    "employment_type": job_data.get("employment_type", Job.EMPLOYMENT_TYPE_INTERNSHIP),
                    "description": job_data.get("description", ""),
                    "posted_at": job_data.get("posted_at"),
                    "source": job_data.get("source", "Example data"),
                    "is_active": True,
                },
            )
            if created:
                created_count += 1

            majors = []
            for key in job_data.get("majors", []):
                major = key_to_major.get(key)
                if major:
                    majors.append(major)
            if majors:
                job.majors.set(majors)

        self.stdout.write(self.style.SUCCESS(f"Seeded example jobs. Created {created_count} new job(s)."))

