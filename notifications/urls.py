"""
Api end points for user_auth module
"""

from django.urls import path
from notifications import views


urlpatterns = [
    path('send_notification_to_admin/', views.send_notification_to_admin, name="send_notification_to_admin"),
    path('send_verification_notification_to_user/', views.send_verification_notification_to_user, name="send_verification_notification_to_user"),
]
