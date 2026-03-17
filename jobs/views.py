"""Jobs page: browse the job market filtered by major, type, salary, and sort."""
import json

from django.db import IntegrityError
from django.shortcuts import render

from career_quiz.quiz_data import get_majors
from .services import fetch_jobs
from .models import JobListingCache


def _save_job_cache(query_hash, query_desc, jobs):
    """
    Insert or update cache. Handles concurrent GETs that would otherwise
    both try create() and hit UNIQUE constraint on query_hash.
    """
    try:
        JobListingCache.objects.create(
            query_hash=query_hash,
            query_desc=query_desc,
            results_json=jobs,
        )
    except IntegrityError:
        row = JobListingCache.objects.get(query_hash=query_hash)
        row.results_json = jobs
        row.query_desc = query_desc
        row.save()  # refreshes fetched_at (auto_now) for TTL


def jobs_home(request):
    majors = get_majors()
    major_labels = {m[0]: m[1] for m in majors}

    major_key = request.GET.get('major', '')
    if not major_key and request.user.is_authenticated:
        try:
            profile = request.user.profile
            major_key = getattr(profile, 'major_key', '') or ''
        except Exception:
            pass
    if not major_key:
        major_key = request.session.get('quiz_major', '')

    job_type = request.GET.get('job_type', '')
    sort = request.GET.get('sort', 'relevance')
    salary_min = request.GET.get('salary_min', '')
    location = request.GET.get('location', '')
    remote_only = request.GET.get('remote') == '1'

    jobs = []
    if major_key:
        cache_hash = JobListingCache.make_hash(
            major=major_key, job_type=job_type, sort=sort,
            salary_min=salary_min, location=location,
            remote='1' if remote_only else '',
        )
        query_desc = f'{major_key} {job_type} {sort}'
        cached = JobListingCache.objects.filter(query_hash=cache_hash).first()
        if cached and not cached.is_stale:
            jobs = cached.results_json
        else:
            jobs = fetch_jobs(
                major_key=major_key, job_type=job_type, sort=sort,
                salary_min=salary_min, location=location,
                remote_only=remote_only,
            )
            _save_job_cache(cache_hash, query_desc, jobs)

    return render(request, 'jobs/home.html', {
        'majors': majors,
        'major_labels_json': json.dumps(major_labels),
        'selected_major': major_key,
        'selected_major_label': major_labels.get(major_key, ''),
        'job_type': job_type,
        'sort': sort,
        'salary_min': salary_min,
        'location': location,
        'remote_only': remote_only,
        'jobs': jobs,
        'jobs_json': json.dumps(jobs),
        'jobs_count': len(jobs),
    })
