"""
Api end points for group challenges module
"""

from django.urls import path
from oneToOneChatModule import views


urlpatterns = [
    path('add_new_chat_between_two_users/', views.add_new_chat_between_two_users, name="add_new_chat_between_two_users"),
    path('display_chat_users_details/', views.display_chat_users_details, name="display_chat_users_details"),
]
