"""
Api end points for app_info_videos module
"""

from django.urls import path

from warriors_workout_videos import views

urlpatterns = [
    path("add_warrior_workout/", views.add_warrior_workout, name="add_warrior_workout"),
    path(
        "get_all_warriors_workout/",
        views.get_all_warriors_workout,
        name="get_all_warriors_workout",
    ),
    # path(
    #     "get_app_info_videos_by_id/",
    #     views.get_app_info_videos_by_id,
    #     name="get_app_info_videos_by_id",
    # ),
    # path(
    #     "delete_all_app_info_videos/",
    #     views.delete_app_info_videos,
    #     name="delete_app_info_videos",
    # ),
    # path(
    #     "delete_app_info_videos_by_id/",
    #     views.delete_app_info_videos_by_id,
    #     name="delete_app_info_videos_by_id",
    # ),
    # path(
    #     "update_app_info_videos/",
    #     views.update_app_info_videos,
    #     name="update_app_info_videos",
    # ),
]
