"""
Api end points for user_auth module
"""

from django.urls import path
from food import views

urlpatterns = [
    path('addFoodType/', views.addFoodType, name="addFoodType"),
    path('addFoodItem/', views.addFoodItem, name="addFoodItem"), 
    path('getAllFoodDishes/', views.getAllFoodDishes, name="getAllFoodDishes"), 
]
