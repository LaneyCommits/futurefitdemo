from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/quiz/", include("apps.quiz.urls")),
    path("api/careers/", include("apps.careers.urls")),
    path("api/users/", include("apps.users.urls")),
]
