"""Serializer for user module"""

from dataclasses import fields
from rest_framework import serializers

from voiceAssistant.models import userPreferredVoiceLanguageModel, voiceAssistantLanguagesModel


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

class AddUserPreferredLanguageSerializer(serializers.ModelSerializer):
    """Serializer for adding user preferred language"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = userPreferredVoiceLanguageModel
        exclude = ["created_at","updated_at"]