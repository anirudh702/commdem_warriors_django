"""Serializer for user module"""

from dataclasses import fields
from rest_framework import serializers

from challenges.models import WorkoutWiseChallengesModel


class GetChallengesdataSerializer(serializers.ModelSerializer):
    """Serializer for getting challenges"""
    user_id = serializers.IntegerField(default=None)
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = WorkoutWiseChallengesModel
        fields = ["user_id"]
