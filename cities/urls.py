"""
Api end points for user_auth module
"""

from django.urls import path

from cities import views

urlpatterns = [
    path("addNewCity/", views.add_new_city, name="addNewCity"),
    path("getAllCities/", views.get_all_cities, name="getAllCities"),
]
