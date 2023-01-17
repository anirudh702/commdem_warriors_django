"""Serializer for user module"""

from dataclasses import fields
from rest_framework import serializers

from oneToOneChatModule.models import OneToOneChatModel

class AddNewChatSerializer(serializers.ModelSerializer):
    """Serializer for adding new chat message / File while one to one chat conversation between users"""
    from_user_id = serializers.IntegerField(default=None)
    to_user_id = serializers.IntegerField(default=None)
    chat_message = serializers.CharField(default=None)
    files_path = serializers.ListField(default=None)
    
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = OneToOneChatModel
        fields = ["from_user_id","to_user_id","chat_message","files_path"]
