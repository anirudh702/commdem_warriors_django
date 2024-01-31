"""Serializer for user module"""

from rest_framework import serializers

from notifications.models import UserPlayerIdModel


class SendNotificationToUserSerializer(serializers.ModelSerializer):
    """Serializer for sending notification to admins once new user signs up"""

    isVerified = serializers.BooleanField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = UserPlayerIdModel
        fields = ["user_id", "isVerified"]
