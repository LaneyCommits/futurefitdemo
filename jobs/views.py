from django.shortcuts import render

from schools.schools_data import get_all_major_labels

from .models import Job


def jobs_home_view(request):
    """
    Simple jobs & internships listing with filters for major, employment type, state, and remote.
    """

    jobs = Job.objects.filter(is_active=True)

    major_key = (request.GET.get("major") or "").strip()
    employment_type = (request.GET.get("type") or "").strip()
    raw_state = (request.GET.get("state") or "").strip()
    # Treat empty / invalid state values as "no preference"
    state = raw_state.upper() if len(raw_state) == 2 else ""
    remote_only = request.GET.get("remote") == "1"

    if major_key:
        jobs = jobs.filter(majors__key=major_key)

    if employment_type:
        jobs = jobs.filter(employment_type=employment_type)

    if state:
        jobs = jobs.filter(state__iexact=state)

    if remote_only:
        jobs = jobs.filter(is_remote=True)

    jobs = jobs.select_related().prefetch_related("majors").distinct()

    majors = get_all_major_labels()

    context = {
        "jobs": jobs,
        "majors": majors,
        "selected_major": major_key,
        "selected_type": employment_type,
        "selected_state": raw_state,
        "remote_only": remote_only,
    }
    return render(request, "jobs/home.html", context)

