from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.register_view, name="users_register"),
    path("login/", views.login_view, name="users_login"),
    path("me/", views.me_view, name="users_me"),
    path("dashboard/", views.dashboard_view, name="users_dashboard"),
]
