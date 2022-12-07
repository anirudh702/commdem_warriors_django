"""Serializer for referral code module"""

from rest_framework import serializers
from referralCode.models import ReferralCodeModel


class AddReferralCodeSerializer(serializers.ModelSerializer):
    """Serializer for adding new referral code details for a specific user"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = ReferralCodeModel
        exclude = ["created_at","updated_at"]


class GetReferralCodeSerializer(serializers.ModelSerializer):
    """Serializer for getting referral code details of a specific user"""
    user_id = serializers.IntegerField(default=None)
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = ReferralCodeModel
        fields = ["user_id"]