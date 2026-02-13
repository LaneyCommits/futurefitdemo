from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('gap-analysis/', views.gap_analysis_view, name='gap_analysis'),
]
