from django.urls import path

from . import views

urlpatterns = [
    path("types/", views.types_view, name="careers_types"),
    path("recommendations/", views.recommendations_view, name="careers_recommendations"),
]
