"""
Api end points for user_auth module
"""

from django.urls import path

from positive_affirmations import views

urlpatterns = [
    path(
        "getPositiveAffirmations/",
        views.getPositiveAffirmations,
        name="getPositiveAffirmations",
    ),
    path(
        "updateUserPositiveAffirmationStatus/",
        views.updateUserPositiveAffirmationStatus,
        name="updateUserPositiveAffirmationStatus",
    ),
]
