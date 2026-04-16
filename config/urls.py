from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import include, path, re_path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/quiz/", include("apps.quiz.urls")),
    path("api/careers/", include("apps.careers.urls")),
    path("api/users/", include("apps.users.urls")),
]


def _spa_index(request):
    """Serve the React SPA for any route not matched by the API or admin."""
    index_html = settings.SPA_DIST_DIR / "index.html"
    if not index_html.is_file():
        if settings.DEBUG:
            return HttpResponseNotFound(
                "frontend/dist/index.html not found. "
                "Run <code>npm run build</code> in the frontend/ directory first, "
                "or use the Vite dev server at <a href='http://localhost:5175'>localhost:5175</a>."
            )
        return HttpResponseNotFound("Not found.")
    return HttpResponse(index_html.read_text(), content_type="text/html")


urlpatterns += [
    re_path(r"^(?!api/|admin/|static/).*$", _spa_index),
]
