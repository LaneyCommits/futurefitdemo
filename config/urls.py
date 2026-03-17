"""
ExploringU URL configuration.

Sections:
  - /               Resume analysis (gap analysis, AI tools)
  - /career-quiz/   Career discovery quiz
  - /resume/        Templates, cover letters, admissions essays, tips
  - /colleges/      School finder
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('resume_analysis.urls')),
    path('career-quiz/', include('career_quiz.urls')),
    path('resume/', include('resume.urls')),
    path('colleges/', include('schools.urls')),
    path('jobs/', include('jobs.urls', namespace='jobs')),
    path('resources/', include('blog.urls')),
    path('accounts/', include('accounts.urls')),
    path('chat/', include('chat.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)