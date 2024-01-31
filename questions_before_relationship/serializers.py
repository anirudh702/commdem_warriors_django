"""Serializer for user module"""

from rest_framework import serializers

from questions_before_relationship.models import QuestionsToAskBeforeModel


class GetAllQuestionsSerializer(serializers.ModelSerializer):
    """Serializer for getting all questions to answer"""

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = QuestionsToAskBeforeModel
        fields = []
