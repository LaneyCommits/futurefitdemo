from django.urls import path

from .views import jobs_home_view


app_name = "jobs"

urlpatterns = [
    path("", jobs_home_view, name="jobs_home"),
]

