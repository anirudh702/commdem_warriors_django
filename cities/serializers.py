"""Serializer for user module"""

from rest_framework import serializers

from location.models import CitiesModel


class AddNewCitySerializer(serializers.ModelSerializer):
    """Serializer for adding new city"""

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = CitiesModel
        exclude = ["created_at", "updated_at"]
