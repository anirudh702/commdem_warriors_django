"""Serializer for user module"""

from rest_framework import serializers

from subscription.models import SubscriptionModel


class AddSubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for adding new subscription details"""

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = SubscriptionModel
        exclude = ["created_at", "updated_at"]


class GetSubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for get subscription details"""

    id = serializers.IntegerField(default=None)
    user_id = serializers.IntegerField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = SubscriptionModel
        fields = ["id", "user_id"]
