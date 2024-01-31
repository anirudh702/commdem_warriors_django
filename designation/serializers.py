"""Serializer for user module"""

from rest_framework import serializers

from designation.models import DesignationModel


class AddDesignationSerializer(serializers.ModelSerializer):
    """Serializer for adding designation"""

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = DesignationModel
        exclude = ["created_at", "updated_at"]


class GetAllDesignationSerializer(serializers.ModelSerializer):
    """Serializer for getting all designations"""

    id = serializers.IntegerField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = DesignationModel
        fields = ["id"]
