"""Serializer for user module"""

from rest_framework import serializers

from location.models import CitiesModel, CountriesModel, StatesModel


class AddNewCitySerializer(serializers.ModelSerializer):
    """Serializer for adding new city"""

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = CitiesModel
        exclude = ["created_at", "updated_at"]


class AddNewStateSerializer(serializers.ModelSerializer):
    """Serializer for adding new state"""

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = StatesModel
        exclude = ["created_at", "updated_at"]


class AddNewCountrySerializer(serializers.ModelSerializer):
    """Serializer for adding new country"""

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = CountriesModel
        exclude = ["created_at", "updated_at"]
