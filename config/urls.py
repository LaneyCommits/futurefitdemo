"""
URL configuration for Student Career Helper.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('resume_analysis.urls')),
    path('career-quiz/', include('career_quiz.urls')),
]
