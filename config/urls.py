"""
ExploringU URL configuration.

Sections:
  - /               Resume analysis (gap analysis, AI tools)
  - /career-quiz/   Career discovery quiz
  - /resume/        Templates, cover letters, admissions essays, tips
  - /colleges/      School finder
  - /jobs/          Job listings
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from config import seo_views

urlpatterns = [
    path('robots.txt', seo_views.robots_txt),
    path('sitemap.xml', seo_views.sitemap_xml),
    path('admin/', admin.site.urls),
    path('', include('resume_analysis.urls')),
    path('career-quiz/', include('career_quiz.urls')),
    path('resume/', include('resume.urls')),
    path('colleges/', include('schools.urls')),
    path('resources/', include('blog.urls')),
    path('accounts/', include('accounts.urls')),
    path('chat/', include('chat.urls')),
    path('jobs/', include('jobs.urls')),
]
if settings.DEBUG:
    # Serves /static/ for any WSGI server (Gunicorn, etc.). runserver also works; without this,
    # DEBUG=True + Gunicorn yields 404 for CSS because only runserver's wrapper serves static by default.
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
