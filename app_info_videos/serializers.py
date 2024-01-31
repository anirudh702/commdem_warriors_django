"""Serializer for app_info_videos module"""

from rest_framework import serializers

from app_info_videos.models import AppInfoVideosModel


class AddAppInfoVideosSerializer(serializers.ModelSerializer):
    """Serializer for adding new app_info_videos details"""

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = AppInfoVideosModel
        exclude = ["created_at", "updated_at"]


class GetAppInfoVideosSerializer(serializers.ModelSerializer):
    """Serializer for get app_info_videos details"""

    id = serializers.IntegerField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = AppInfoVideosModel
        fields = ["id"]
