"""
Api end points for user_auth module
"""

from django.urls import path
from user import views


urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),  
    path('updateProfile/', views.updateProfile, name="update_profile"),  
    path('getUserProfile/', views.getUserProfileDetails, name="getUserProfileDetails"),  
    path('is_user_subscribed/', views.is_user_subscribed, name="is_user_subscribed"),  
    path('addPayment/', views.addNewPayment, name="addPayment"),   
    path('addNewSubscription/', views.addNewSubscription, name="addNewSubscription"),   
    path('getUserSubscriptionById/', views.getUserSubscriptionById, name="getUserSubscriptionById"),   
    path('getUserSubscriptionById/', views.getUserSubscriptionById, name="getUserSubscriptionById"),   
    path('getAllUsersDetails/', views.getAllUsersDetails, name="getAllUsersDetails"),
    path('getOverallPerformerOfTheWeek/', views.getOverallPerformerOfTheWeek, name="getOverallPerformerOfTheWeek"),   
    path('getOverallPerformerOfTheWeekCategoryWise/', views.getOverallPerformerOfTheWeekCategoryWise, name="getOverallPerformerOfTheWeekCategoryWise"),   
]
