"""Chat app URLs."""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_home_view, name='chat_home'),
    path('api/messages/', views.chat_messages_view, name='chat_messages'),
    path('api/send/', views.chat_send_view, name='chat_send'),
]
