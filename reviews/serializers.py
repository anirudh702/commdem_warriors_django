
"""Serializer for review module"""

from rest_framework import serializers

from reviews.models import ReviewModel


class AddReviewSerializer(serializers.ModelSerializer):
    """Serializer for adding new review details"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = ReviewModel
        exclude = ["created_at","updated_at"]


class GetReviewSerializer(serializers.ModelSerializer):
    """Serializer for get review details"""
    id = serializers.IntegerField(default=None)
    user_id = serializers.IntegerField(default=None)
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = ReviewModel
        fields = ["id","user_id"]

                  