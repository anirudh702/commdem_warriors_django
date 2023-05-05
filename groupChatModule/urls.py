"""
Api end points for group challenges module
"""

from django.urls import path
from groupChatModule import views


urlpatterns = [
#     path('add_new_chat_in_group_chat/', views.add_new_chat_between_two_users, name="add_new_chat_in_group_chat"),
#     path('get_all_chats/', views.display_chat_users_details, name="get_all_chats"),
path('add_group_chat_file/', views.add_group_chat_file, name="add_group_chat_file"),
]
