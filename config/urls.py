"""
FutureFit URL configuration.

Sections:
  - /               Resume analysis (gap analysis, AI tools)
  - /career-quiz/   Career discovery quiz
  - /resume/        Templates, cover letters, admissions essays, tips
  - /colleges/      School finder
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('resume_analysis.urls')),
    path('career-quiz/', include('career_quiz.urls')),
    path('resume/', include('resume.urls')),
    path('colleges/', include('schools.urls')),
]
