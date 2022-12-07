"""Serializer for user module"""

from dataclasses import fields
from rest_framework import serializers
from income.models import IncomeModel


class AddIncomeRangeSerializer(serializers.ModelSerializer):
    """Serializer for adding new income range"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = IncomeModel
        exclude = ["created_at","updated_at"]
