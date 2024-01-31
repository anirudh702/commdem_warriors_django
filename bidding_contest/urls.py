"""
Api end points for group challenges module
"""

from django.urls import path

from bidding_contest import views

urlpatterns = [
    path(
        "get_bidding_contest_details/",
        views.get_bidding_contest_details,
        name="get_bidding_contest_details",
    ),
    path(
        "add_participant_in_bidding_contest/",
        views.add_participant_in_bidding_contest,
        name="add_participant_in_bidding_contest",
    ),
    path(
        "update_participant_details_in_bidding_contest/",
        views.update_participant_details_in_bidding_contest,
        name="update_participant_details_in_bidding_contest",
    ),
]
