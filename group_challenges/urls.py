"""
Api end points for group challenges module
"""

from django.urls import path

from group_challenges import views

urlpatterns = [
    path(
        "get_group_challenges/",
        views.get_group_challenges,
        name="get_group_challenges",
    ),
    path(
        "get_all_public_custom_group_challenges_title/",
        views.get_all_public_custom_group_challenges_title,
        name="get_all_public_custom_group_challenges_title",
    ),
    path(
        "get_all_participants_of_group_challenge/",
        views.get_all_participants_of_group_challenge,
        name="get_all_participants_of_group_challenge",
    ),
    path(
        "add_user_in_group_challenge/",
        views.add_user_in_group_challenge,
        name="add_user_in_group_challenge",
    ),
    path(
        "add_new_public_custom_group_challenge/",
        views.add_new_public_custom_group_challenge,
        name="add_new_public_custom_group_challenge",
    ),
    path(
        "add_new_private_custom_group_challenge/",
        views.add_new_private_custom_group_challenge,
        name="add_new_private_custom_group_challenge",
    ),
    path(
        "upload_video_for_group_challenge/",
        views.upload_video_for_group_challenge,
        name="upload_video_for_group_challenge",
    ),
    # path('update_user_participation_for_group_challenge/', views.update_user_participation_for_group_challenge, name="update_user_participation_for_group_challenge"),
]
