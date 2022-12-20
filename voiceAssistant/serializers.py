"""Serializer for user module"""

from dataclasses import fields
from rest_framework import serializers

from voiceAssistant.models import userCommitmentVoiceBeforeUpdateModel, userPreferredVoiceLanguageModel, voiceAssistantLanguagesModel


class AddNewLanguageSerializer(serializers.ModelSerializer):
    """Serializer for adding new language for voice assistant"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = voiceAssistantLanguagesModel
        exclude = ["created_at","updated_at"]

class GetAllLanguagesSerializer(serializers.ModelSerializer):
    """Serializer for getting all languages"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = voiceAssistantLanguagesModel
        exclude = ["created_at","updated_at"]

class AddUserCommitmentVoiceFileSerializer(serializers.ModelSerializer):
    """Serializer for adding user commitment voice file"""
    user_id = serializers.IntegerField()
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = userCommitmentVoiceBeforeUpdateModel
        fields = ["user_id"]