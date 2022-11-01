"""
Api end points for user_auth module
"""

from django.urls import path
from subscription import views


urlpatterns = [
    path('add_subscription/', views.add_subscription, name="add_subscription"),
    path('get_all_subscriptions/', views.get_all_subscriptions, name="get_all_subscriptions"),
    path('get_subscription_by_id/', views.get_subscription_by_id, name="get_subscription_by_id"),
]
