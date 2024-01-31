"""
Api end points for user_auth module
"""

from django.urls import path

from location import views

urlpatterns = [
    # path('addCountryDialCodes/', views.addCountryDialCodes, name="addCountryDialCodes"),
    path("get_all_countries/", views.get_all_countries, name="get_all_countries"),
    path(
        "get_all_states_of_country/",
        views.get_all_states_of_country,
        name="get_all_states_of_country",
    ),
    path(
        "get_all_cities_of_state/",
        views.get_all_cities_of_state,
        name="get_all_cities_of_state",
    ),
]
