from django.urls import path
from . import views

urlpatterns = [
    path('', views.QuizHomeView.as_view(), name='career_quiz_home'),
    path('take/', views.quiz_view, name='career_quiz_take'),
    path('results/', views.quiz_results_view, name='career_quiz_results'),
]
