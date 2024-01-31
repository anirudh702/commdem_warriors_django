"""
Api end points for user_auth module
"""

from django.urls import path

from advertisement import views

urlpatterns = [
    path(
        "add_new_advertisement/",
        views.add_new_advertisement,
        name="add_new_advertisement",
    ),
    path(
        "add_advertisement_logs/",
        views.add_advertisement_logs,
        name="add_advertisement_logs",
    ),
    path(
        "update_advertisement/",
        views.update_advertisement,
        name="update_advertisement",
    ),
    path(
        "get_all_advertisements/",
        views.get_all_advertisements,
        name="get_all_advertisements",
    ),
    path(
        "delete_advertisement/",
        views.delete_advertisement,
        name="delete_advertisement",
    ),
    path(
        "add_new_advertisement_click/",
        views.add_new_advertisement_click,
        name="add_new_advertisement_click",
    ),
    path(
        "add_new_advertisement_view/",
        views.add_new_advertisement_view,
        name="add_new_advertisement_view",
    ),
]
