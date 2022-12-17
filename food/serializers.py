"""Serializer for user module"""

from dataclasses import fields
from rest_framework import serializers

from food.models import TypeOfFoodModel,FoodModel


class TypeOfFoodSerializer(serializers.ModelSerializer):
    """Serializer for adding type of food"""

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = TypeOfFoodModel
        exclude = ["created_at","updated_at"]


class AddFoodSerializer(serializers.ModelSerializer):
    """Serializer for adding food details"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = FoodModel
        exclude = ["created_at","updated_at"]

class GetAllFoodDishesSerializer(serializers.ModelSerializer):
    """Serializer to get all food dishes"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = FoodModel
        exclude = ["created_at","updated_at"]