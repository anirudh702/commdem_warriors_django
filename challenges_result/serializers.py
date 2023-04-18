
"""Serializer for challenges_result module"""

from rest_framework import serializers

from challenges_result.models import ChallengesResultModel


class AddChallengesResultSerializer(serializers.ModelSerializer):
    """Serializer for adding new challenges_result details"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = ChallengesResultModel
        exclude = ["created_at","updated_at"]


class GetChallengesResultSerializer(serializers.ModelSerializer):
    """Serializer for get challenges_result details"""
    competition_id = serializers.IntegerField(default=None)
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = ChallengesResultModel
        fields = ["competition_id"]

                  