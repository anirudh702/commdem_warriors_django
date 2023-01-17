"""
Api end points for group challenges module
"""

from django.urls import path
from oneToOneChatModule import views


urlpatterns = [
    path('add_new_chat_between_two_users/', views.add_new_chat_between_two_users, name="add_new_chat_between_two_users"),
]
