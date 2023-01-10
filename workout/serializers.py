"""Serializer for user module"""

from dataclasses import fields
from rest_framework import serializers

from workout.models import WorkoutModel


class GetWorkoutdataSerializer(serializers.ModelSerializer):
    """Serializer for getting challenges"""
    user_id = serializers.IntegerField(default=None)
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = WorkoutModel
        fields = ["user_id"]
