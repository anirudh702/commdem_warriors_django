"""
Api end points for user_auth module
"""

from django.urls import path

from referralCode import views

urlpatterns = [
    path(
        "get_referral_code_of_user/",
        views.get_referral_code_of_user,
        name="get_referral_code_of_user",
    ),
    path(
        "get_all_referrals_of_user/",
        views.get_all_referrals_of_user,
        name="get_all_referrals_of_user",
    ),
    path(
        "delete_referral_code_of_user/",
        views.delete_referral_code_of_user,
        name="delete_referral_code_of_user",
    ),
]
