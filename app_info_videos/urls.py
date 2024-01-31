"""
Api end points for app_info_videos module
"""

from django.urls import path

from app_info_videos import views

urlpatterns = [
    path("add_app_info_videos/", views.add_app_info_videos, name="add_app_info_videos"),
    path(
        "get_app_info_videos/",
        views.get_all_app_info_videos,
        name="get_app_info_videos",
    ),
    path(
        "delete_all_app_info_videos/",
        views.delete_all_app_info_videos,
        name="delete_app_info_videos",
    ),
    path(
        "delete_app_info_videos_by_id/",
        views.delete_app_info_videos_by_id,
        name="delete_app_info_videos_by_id",
    ),
    path(
        "update_app_info_videos/",
        views.update_app_info_videos,
        name="update_app_info_videos",
    ),
]
