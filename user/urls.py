"""
Api end points for user_auth module
"""

from django.urls import path
from user import views

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('delete_user/', views.delete_user_details, name="delete_user_details"),
    path('signin/', views.signin, name="signin"),
    path('makeUserAdmin/', views.makeUserAdmin, name="makeUserAdmin"),  
    path('updateProfile/', views.updateProfile, name="update_profile"),  
    path('updateUserPrivacyDetails/', views.updateUserPrivacyDetails, name="updateUserPrivacyDetails"),  
    path('getUserPrivacyDetails/', views.getUserPrivacyDetails, name="getUserPrivacyDetails"),
    path('updateIndividualUserWisePrivacyDetails/', views.updateIndividualUserWisePrivacyDetails, name="updateIndividualUserWisePrivacyDetails"),  
    path('getIndividualUserWisePrivacyDetails/', views.getIndividualUserWisePrivacyDetails, name="getIndividualUserWisePrivacyDetails"),
    path('getUserProfile/', views.getUserProfileDetails, name="getUserProfileDetails"),  
    path('is_user_subscribed/', views.is_user_subscribed, name="is_user_subscribed"),  
    path('addPayment/', views.addNewPayment, name="addPayment"),   
    # path('addNewSubscription/', views.addNewSubscription, name="addNewSubscription"),   
    path('getUserSubscriptionById/', views.getUserSubscriptionById, name="getUserSubscriptionById"),   
    path('getAllUsersDetails/', views.getAllUsersDetails, name="getAllUsersDetails"),
    path('getAllUnVerifiedUsers/', views.getAllUnVerifiedUsers, name="getAllUnVerifiedUsers"),
    path('getOverallPerformerOfTheWeek/', views.getOverallPerformerOfTheWeek, name="getOverallPerformerOfTheWeek"),  
    path('getAllDataOfOverallPerformers/', views.getAllDataOfOverallPerformers, name="getAllDataOfOverallPerformers"),   
    path('getOverallPerformerOfTheWeekCategoryWise/', views.getOverallPerformerOfTheWeekCategoryWise, name="getOverallPerformerOfTheWeekCategoryWise"),
    path('addNewReviewOfUser/', views.addNewReviewOfUser, name="addNewReviewOfUser"),
    path('updateUserReview/', views.updateUserReview, name="updateUserReview"),
    path('deleteUserReview/', views.deleteUserReview, name="deleteUserReview"),
    path('get_reviews_of_all_users/', views.get_reviews_of_all_users, name="get_reviews_of_all_users"),
]
