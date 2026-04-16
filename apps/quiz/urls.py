from django.urls import path

from . import views

urlpatterns = [
    path("questions/", views.questions_view, name="quiz_questions"),
    path("submit/", views.submit_view, name="quiz_submit"),
]
