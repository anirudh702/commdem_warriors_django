"""
Api end points for user_auth module
"""

from django.urls import path
from user import views


urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),  
    path('addPayment/', views.addNewPayment, name="addPayment"),   
]
