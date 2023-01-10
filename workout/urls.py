"""
Api end points for user_auth module
"""

from django.urls import path
from workout import views


urlpatterns = [
    path('get_workout_of_today_of_user/', views.get_workout_of_today_of_user, name="get_workout_of_today_of_user"),
]
