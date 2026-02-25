"""Career quiz app URLs: home, choose path, take quiz, explore, results."""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_home_view, name='career_quiz_home'),
    path('choose-path/', views.choose_path_view, name='career_quiz_choose_path'),
    path('about/', views.about_view, name='career_quiz_about'),
    path('how-it-works/', views.how_it_works_view, name='career_quiz_how_it_works'),
    path('pick-major/', views.major_selection_view, name='career_quiz_major'),
    path('take/', views.quiz_view, name='career_quiz_take'),
    path('results/', views.quiz_results_view, name='career_quiz_results'),
    path('explore/', views.explore_quiz_view, name='career_quiz_explore'),
    path('explore/results/', views.explore_results_view, name='career_quiz_explore_results'),
    path('results-for/<str:major_key>/', views.results_for_major_view, name='career_quiz_results_for_major'),
]
