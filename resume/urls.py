from django.urls import path
from . import views

urlpatterns = [
    path('', views.resume_home_view, name='resume_home'),
    path('templates/', views.resume_templates_view, name='resume_templates'),
    path('templates/<str:major_key>/', views.resume_template_detail_view, name='resume_template_detail'),
    path('tips/', views.resume_tips_view, name='resume_tips'),
    path('ai-tools/', views.resume_ai_tools_view, name='resume_ai_tools'),

    # AI API endpoints
    path('api/ai/status/', views.ai_status_view, name='resume_ai_status'),
    path('api/ai/enhance-bullet/', views.ai_enhance_bullet_view, name='resume_ai_enhance_bullet'),
    path('api/ai/generate-summary/', views.ai_generate_summary_view, name='resume_ai_generate_summary'),
    path('api/ai/suggest-skills/', views.ai_suggest_skills_view, name='resume_ai_suggest_skills'),
    path('api/ai/tailor-resume/', views.ai_tailor_resume_view, name='resume_ai_tailor_resume'),
    path('api/ai/review-resume/', views.ai_review_resume_view, name='resume_ai_review_resume'),
]
