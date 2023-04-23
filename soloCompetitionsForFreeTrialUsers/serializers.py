"""Serializer for user module"""

from dataclasses import fields
from rest_framework import serializers

from soloCompetitionsForFreeTrialUsers.models import FreeTrialSoloChallengesModel

class GetSoloChallengesSerializer(serializers.ModelSerializer):
    """Serializer for getting solo challenges for free trial users"""
    user_id = serializers.IntegerField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = FreeTrialSoloChallengesModel
        fields = ["user_id"]

class UploadVideoOfUserSoloChallengeSerializer(serializers.ModelSerializer):
    """Serializer for uploading challenge video of a user"""
    user_id = serializers.IntegerField(default=None)
    solo_challenge_id = serializers.IntegerField(default=None)
    video_file = serializers.FileField(default=None)
    is_updated_file = serializers.BooleanField(default=False)

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = FreeTrialSoloChallengesModel
        fields = ["user_id",'solo_challenge_id','video_file','is_updated_file']
