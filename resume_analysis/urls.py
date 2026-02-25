"""Resume analysis app URLs: home (gap analysis, AI tools)."""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
]
