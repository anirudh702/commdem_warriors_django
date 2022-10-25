"""Serializer for user module"""

from dataclasses import fields
from rest_framework import serializers
from commitment.models import CommitmentCategoryModel, CommitmentModel, CommitmentNameModel


class AddCommitmentSerializer(serializers.ModelSerializer):
    """Serializer for adding new commitment"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = CommitmentModel
        exclude = ["created_at","updated_at","commitment_date","is_done"]


class AddCommitmentCategorySerializer(serializers.ModelSerializer):
    """Serializer for adding new commitment category"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = CommitmentCategoryModel
        exclude = ["created_at","updated_at"]

class AddCommitmentNameSerializer(serializers.ModelSerializer):
    """Serializer for adding new commitment name"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = CommitmentNameModel
        exclude = ["created_at","updated_at"]

class GetCommitmentCategorySerializer(serializers.ModelSerializer):
    """Serializer for getting commitment category"""
    id = serializers.IntegerField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = CommitmentCategoryModel
        fields = ["id"]

class GetCommitmentNameSerializer(serializers.ModelSerializer):
    """Serializer for getting commitment name"""
    # id = serializers.IntegerField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = CommitmentNameModel
        fields = ["category"]

class GetCommitmentsSerializer(serializers.ModelSerializer):
    """Serializer for getting commitments"""
    # id = serializers.IntegerField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = CommitmentModel
        fields = ["user","commitment_date"]
        