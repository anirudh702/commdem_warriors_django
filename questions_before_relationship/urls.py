"""
Api end points for user_auth module
"""

from django.urls import path

from questions_before_relationship import views

urlpatterns = [
    path("get_all_questions/", views.get_all_questions, name="get_all_questions"),
    path("get_my_maches/", views.get_my_maches, name="get_my_maches"),
    # path('get_all_subscriptions/', views.get_all_subscriptions, name="get_all_subscriptions"),
    # path('get_subscription_by_id/', views.get_subscription_by_id, name="get_subscription_by_id"),
    # path('get_past_subscriptions_of_user/', views.get_past_subscriptions_of_user, name="get_past_subscriptions_of_user"),
]
