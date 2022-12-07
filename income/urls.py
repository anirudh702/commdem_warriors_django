"""
Api end points for user_auth module
"""

from django.urls import path
from income import views


urlpatterns = [
    path('addNewIncome/', views.add_new_income_range, name="addNewIncome"),
    path('getAllIncome/', views.get_all_income_range, name="getAllIncome"),   
]
