"""Serializer for challenges_result module"""

from rest_framework import serializers

from challenges_result.models import ChallengesResultModel


class AddChallengesResultSerializer(serializers.ModelSerializer):
    """Serializer for adding new challenges_result details"""

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = ChallengesResultModel
        exclude = ["created_at", "updated_at"]


class GetChallengesResultSerializer(serializers.ModelSerializer):
    """Serializer for get challenges_result details"""

    group_challenge_id = serializers.IntegerField(default=None)
    search_param = serializers.CharField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = ChallengesResultModel
        fields = ["group_challenge_id", "search_param"]


class GetChallengesResultOfUserSerializer(serializers.ModelSerializer):
    """Serializer for get challenges_result details of a user"""

    user_id = serializers.IntegerField(default=None)
    group_challenge_id = serializers.IntegerField(default=None)
    challenge_type = serializers.CharField(default=None)
    sort_by = serializers.CharField(default=None)
    challenge_date = serializers.CharField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = ChallengesResultModel
        fields = [
            "user_id",
            "challenge_type",
            "group_challenge_id",
            "sort_by",
            "challenge_date",
        ]
