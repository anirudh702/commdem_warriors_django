"""Serializer for user module"""

from rest_framework import serializers

from groupChatModule.models import GroupChatModel


class AddNewChatSerializer(serializers.ModelSerializer):
    """Serializer for adding new chat message / File while group chat conversation"""

    from_user_id = serializers.IntegerField(default=None)
    chat_message = serializers.CharField(default=None)
    files_path = serializers.ListField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = GroupChatModel
        fields = ["from_user_id", "chat_message", "files_path"]
