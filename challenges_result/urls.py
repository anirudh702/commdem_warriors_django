"""
Api end points for challenges_result module
"""

from django.urls import path

from challenges_result import views

urlpatterns = [
    path(
        "add_challenges_result/",
        views.add_challenges_result,
        name="add_challenges_result",
    ),
    path(
        "get_all_challenges_result_of_user/",
        views.get_all_challenges_result_of_user,
        name="get_all_challenges_result_of_user",
    ),
    path(
        "get_challenges_result_by_id/",
        views.get_challenges_result_by_id,
        name="get_challenges_result_by_id",
    ),
    path(
        "delete_all_challenges_result/",
        views.delete_all_challenges_result,
        name="delete_all_challenges_result",
    ),
    path(
        "delete_challenges_result_by_id/",
        views.delete_challenges_result_by_id,
        name="delete_challenges_result_by_id",
    ),
    path(
        "update_challenges_result/",
        views.update_challenges_result,
        name="update_challenges_result",
    ),
]
