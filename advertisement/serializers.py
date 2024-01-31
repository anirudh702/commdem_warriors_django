"""Serializer for user module"""

from rest_framework import serializers

from advertisement.models import (
    AdvertisementClicksModel,
    AdvertisementModel,
    AdvertisementViewsModel,
)


class AddAdvertisementSerializer(serializers.ModelSerializer):
    """Serializer for adding advertisement"""

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = AdvertisementModel
        exclude = ["created_at", "updated_at"]


class UpdateAdvertisementSerializer(serializers.ModelSerializer):
    """Serializer for updating advertisement details"""

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = AdvertisementModel
        exclude = ["created_at", "updated_at"]


class GetAdvertisementsSerializer(serializers.ModelSerializer):
    """Serializer for getting all advertisements"""

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = AdvertisementModel
        fields = []


class AddAdvertisementClickSerializer(serializers.ModelSerializer):
    """Serializer for adding click of an advertisement"""

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = AdvertisementClicksModel
        exclude = ["created_at", "updated_at", "is_active"]


class AddAdvertisementViewSerializer(serializers.ModelSerializer):
    """Serializer for adding view of an advertisement"""

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = AdvertisementViewsModel
        exclude = ["created_at", "updated_at", "is_active"]


class DeleteAdvertisementSerializer(serializers.ModelSerializer):
    """Serializer for deleting an advertisement"""

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = AdvertisementModel
        fields = ["id"]
