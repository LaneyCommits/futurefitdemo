from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('verify-email-sent/', views.verify_email_sent_view, name='verify_email_sent'),
    path('verify-email/<str:key>/', views.verify_email_view, name='verify_email'),
    path('verify-email-done/', views.verify_email_done_view, name='verify_email_done'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/personalization/', views.personalization_view, name='personalization'),
]
