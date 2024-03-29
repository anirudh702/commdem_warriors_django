"""Serializer for user module"""

from dataclasses import fields
from rest_framework import serializers
from commitment.models import CauseOfCategorySuccessOrFailureModel, CommitmentCategoryModel, CommitmentModel, CommitmentNameModel


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
    commitment_date = serializers.CharField(default=None)
    title_message = serializers.CharField(default=None)
    start_date = serializers.CharField(default=None)
    end_date = serializers.CharField(default=None)
    search_param = serializers.CharField(default=None)
    page_no = serializers.IntegerField(default=None)
    page_size = serializers.IntegerField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = CommitmentModel
        fields = ["user_id","commitment_date",'start_date','end_date','page_no','page_size','search_param','title_message']
        
class UpdateCommitmentsSerializer(serializers.ModelSerializer):
    """Serializer for updating commitments"""
    id = serializers.IntegerField()
    cause_id = serializers.CharField()

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = CommitmentModel
        fields = ["user_id","id","is_done","cause_id"]

class GetOtherUsersCommitmentsSerializer(serializers.ModelSerializer):
    """Serializer for getting commitments of other users"""
    page_no = serializers.IntegerField(default=None)
    page_size = serializers.IntegerField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = CommitmentModel
        fields = ["user_id","page_no","page_size"]

class AddCauseOfCategorySerializer(serializers.ModelSerializer):
    """Serializer for adding cause of category data success/failure"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = CauseOfCategorySuccessOrFailureModel
        exclude = ["created_at","updated_at"]

    
class GetCauseOfCategorySerializer(serializers.ModelSerializer):
    """Serializer for getting cause of category success or failure"""
    is_success = serializers.BooleanField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = CauseOfCategorySuccessOrFailureModel
        fields = ["is_success","category"]