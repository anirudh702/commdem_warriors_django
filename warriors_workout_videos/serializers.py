"""Serializer for app_info_videos module"""

from rest_framework import serializers

from warriors_workout_videos.models import WarriorsWorkoutVideosModel


class AddWarriorsWorkoutVideoSerializer(serializers.ModelSerializer):
    """Serializer for adding new workout details of warrior"""

    user_id = serializers.IntegerField(default=None)
    commitment_id = serializers.IntegerField(default=None)
    workout_file = serializers.FileField(default=None)
    description = serializers.CharField(default="")

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = WarriorsWorkoutVideosModel
        fields = ["user_id", "commitment_id", "workout_file", "description"]


class GetWarriorsWorkoutVideoSerializer(serializers.ModelSerializer):
    """Serializer for getting workout details of warrior"""

    user_id = serializers.IntegerField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = WarriorsWorkoutVideosModel
        fields = ["user_id"]
