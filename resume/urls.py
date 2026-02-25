"""
Resume & Writing app URLs.

Sections:
  - Document types: resume, cover letters, admissions essays (templates)
  - Pages: home, tips, AI tools, generate
  - API: template/cover-letter HTML, PDF generation, AI endpoints
"""
from django.urls import path
from . import views

# ---------------------------------------------------------------------------
# Document type pages (Resume, Cover Letters, Admissions Essays)
# ---------------------------------------------------------------------------
urlpatterns = [
    path('', views.resume_home_view, name='resume_home'),
    path('templates/', views.resume_templates_view, name='resume_templates'),
    path('cover-letters/', views.resume_templates_view, {'doc_type': 'cover_letter'}, name='resume_cover_letters'),
    path('admissions-essays/', views.resume_templates_view, {'doc_type': 'admissions_essay'}, name='resume_admissions_essays'),
    path('templates/<str:major_key>/', views.resume_template_detail_view, name='resume_template_detail'),
    path('tips/', views.resume_tips_view, name='resume_tips'),
    path('ai-tools/', views.resume_ai_tools_view, name='resume_ai_tools'),
    path('generate/', views.resume_generate_view, name='resume_generate'),
    # API: template/cover-letter HTML, PDF
    path('api/pdf/', views.resume_pdf_view, name='resume_pdf'),
    path('api/template/<str:major_key>/', views.resume_template_html_view, name='resume_template_html'),
    path('api/cover-letter/<str:major_key>/', views.resume_cover_letter_html_view, name='resume_cover_letter_html'),
    path('api/generate-pdf/', views.resume_generate_pdf_view, name='resume_generate_pdf'),
    # AI API endpoints
    path('api/ai/status/', views.ai_status_view, name='resume_ai_status'),
    path('api/ai/extract-pdf/', views.ai_extract_pdf_view, name='resume_ai_extract_pdf'),
    path('api/ai/generate-content/', views.ai_generate_content_view, name='resume_ai_generate_content'),
    path('api/ai/enhance-bullet/', views.ai_enhance_bullet_view, name='resume_ai_enhance_bullet'),
    path('api/ai/generate-summary/', views.ai_generate_summary_view, name='resume_ai_generate_summary'),
    path('api/ai/suggest-skills/', views.ai_suggest_skills_view, name='resume_ai_suggest_skills'),
    path('api/ai/tailor-resume/', views.ai_tailor_resume_view, name='resume_ai_tailor_resume'),
    path('api/ai/review-resume/', views.ai_review_resume_view, name='resume_ai_review_resume'),
    path('api/ai/enhance-resume/', views.ai_enhance_resume_view, name='resume_ai_enhance_resume'),
]
