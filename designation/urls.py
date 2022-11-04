"""
Api end points for user_auth module
"""

from django.urls import path
from designation import views


urlpatterns = [
    path('addNewDesignation/', views.addNewDesignation, name="addNewDesignation"),
    path('getAllDeisgnations/', views.getAllDeisgnations, name="getAllDeisgnations"),  
]
