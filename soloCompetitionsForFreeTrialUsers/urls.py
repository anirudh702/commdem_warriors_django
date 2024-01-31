"""
Api end points for group challenges module
"""

from django.urls import path

from soloCompetitionsForFreeTrialUsers import views

urlpatterns = [
    path(
        "get_all_solo_challenges/",
        views.get_all_solo_challenges,
        name="get_all_solo_challenges",
    ),
    path(
        "upload_video_for_solo_challenge/",
        views.upload_video_for_solo_challenge,
        name="upload_video_for_solo_challenge",
    ),
]
