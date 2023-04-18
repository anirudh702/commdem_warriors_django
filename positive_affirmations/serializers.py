"""Serializer for user module"""

from dataclasses import fields
from rest_framework import serializers
from commitment.models import CauseOfCategorySuccessOrFailureModel, CommitmentCategoryModel, CommitmentModel, CommitmentNameModel, UserCommitmentsForNextWeekModel
from positive_affirmations.models import PositiveAffirmationModel, UserAffirmationModel


class GetPositiveAffirmationsSerializer(serializers.ModelSerializer):
    """Serializer for getting positive affirmation"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = PositiveAffirmationModel
        fields = [""]

class UpdateUserPositiveAffirmationsSerializer(serializers.ModelSerializer):
    """Serializer for updating user positive affirmation"""
    user_id = serializers.IntegerField(default=None)
    number_of_commitment_for_week_id = serializers.IntegerField(default=None)
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = UserAffirmationModel
        fields = ["number_of_commitment_for_week_id","user_id"]