"""Serializer for user module"""

from dataclasses import fields
from rest_framework import serializers

from group_challenges.models import GroupChallengesModel

class GetGroupChallengesSerializer(serializers.ModelSerializer):
    """Serializer for getting group challenges"""
    date = serializers.CharField(default=None)
    page_no = serializers.IntegerField(default=None)
    page_size = serializers.IntegerField(default=None)
    user_id = serializers.IntegerField(default=None)
    is_finished = serializers.BooleanField(default=None)
    is_ongoing = serializers.BooleanField(default=None)
    is_upcoming = serializers.BooleanField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = GroupChallengesModel
        fields = ["user_id",'page_no','page_size','date','is_finished','is_ongoing','is_upcoming']

class GetAllParticipantsOfGroupChallengeSerializer(serializers.ModelSerializer):
    """Serializer for getting all participants in group challenge"""
    page_no = serializers.IntegerField(default=None)
    page_size = serializers.IntegerField(default=None)
    group_challenge_id = serializers.IntegerField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = GroupChallengesModel
        fields = ["group_challenge_id",'page_no','page_size']

class AddNewUserInGroupChallengeSerializer(serializers.ModelSerializer):
    """Serializer for adding a new user in group challenge"""
    user_id = serializers.IntegerField(default=None)
    group_challenge_id = serializers.IntegerField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = GroupChallengesModel
        fields = ["user_id",'group_challenge_id']

class UploadVideoOfUserGroupChallengeSerializer(serializers.ModelSerializer):
    """Serializer for uploading challenge video of a user"""
    user_id = serializers.IntegerField(default=None)
    group_challenge_id = serializers.IntegerField(default=None)
    video_file = serializers.FileField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = GroupChallengesModel
        fields = ["user_id",'group_challenge_id','video_file']

class UpdateUserParticipationStatusInGroupChallengeSerializer(serializers.ModelSerializer):
    """Serializer for update user participation in a group challenge"""
    user_id = serializers.IntegerField(default=None)
    group_challenge_id = serializers.IntegerField(default=None)
    want_to_participate = serializers.BooleanField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = GroupChallengesModel
        fields = ["user_id",'group_challenge_id','want_to_participate']