"""Serializer for user module"""

from rest_framework import serializers

from group_challenges.models import (
    GroupChallengeModel,
    PublicCustomGroupChallengesTitleModel,
)


class GetGroupChallengesSerializer(serializers.ModelSerializer):
    """Serializer for getting group challenges"""

    page_no = serializers.IntegerField(default=None)
    page_size = serializers.IntegerField(default=None)
    user_id = serializers.IntegerField(default=None)
    min_rating = serializers.IntegerField(default=None)
    max_rating = serializers.IntegerField(default=None)
    is_finished = serializers.BooleanField(default=None)
    is_ongoing = serializers.BooleanField(default=None)
    is_my_challenges = serializers.BooleanField(default=None, allow_null=True)
    is_upcoming = serializers.BooleanField(default=None)
    sort_by = serializers.CharField(default=None)
    age_group = serializers.CharField(default=None)
    start_date = serializers.CharField(default=None)
    end_date = serializers.CharField(default=None)
    gender = serializers.CharField(default=None)
    challenge_type = serializers.CharField(default="")

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = GroupChallengeModel
        fields = [
            "is_my_challenges",
            "challenge_type",
            "gender",
            "start_date",
            "end_date",
            "user_id",
            "page_no",
            "page_size",
            "is_finished",
            "is_ongoing",
            "is_upcoming",
            "sort_by",
            "age_group",
            "min_rating",
            "max_rating",
        ]


class GetAllParticipantsOfGroupChallengeSerializer(serializers.ModelSerializer):
    """Serializer for getting all participants in group challenge"""

    page_no = serializers.IntegerField(default=None)
    page_size = serializers.IntegerField(default=None)
    group_challenge_id = serializers.IntegerField(default=None)
    challenge_type = serializers.CharField(default="")

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = GroupChallengeModel
        fields = ["group_challenge_id", "page_no", "page_size", "challenge_type"]


class AddNewUserInGroupChallengeSerializer(serializers.ModelSerializer):
    """Serializer for adding a new user in group challenge"""

    user_id = serializers.IntegerField(default=None)
    group_challenge_id = serializers.IntegerField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = GroupChallengeModel
        fields = ["user_id", "group_challenge_id"]


class CreateNewGroupChallengeSerializer(serializers.ModelSerializer):
    """Serializer for creating new public custom group challenge"""

    user_id = serializers.IntegerField(default=None)
    host_user_id = serializers.IntegerField(default=None)
    challenge_details_id = serializers.IntegerField(default=None)
    payment_id = serializers.CharField(default=None)
    max_participants_allowed = serializers.IntegerField(default=None)
    price_to_pay = serializers.CharField(default=None)
    challenge_date = serializers.DateField(default=None)
    challenge_type = serializers.CharField(default="")
    participants = serializers.ListField(default=[])
    is_edit = serializers.BooleanField(default=False)

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = GroupChallengeModel
        fields = [
            "user_id",
            "challenge_details_id",
            "payment_id",
            "max_participants_allowed",
            "price_to_pay",
            "challenge_date",
            "challenge_type",
        ]


class UploadVideoOfUserGroupChallengeSerializer(serializers.ModelSerializer):
    """Serializer for uploading challenge video of a user"""

    user_id = serializers.IntegerField(default=None)
    group_challenge_id = serializers.IntegerField(default=None)
    total_number = serializers.IntegerField(default=None)
    video_file = serializers.FileField(default=None)
    is_updated_file = serializers.BooleanField(default=False)

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = GroupChallengeModel
        fields = [
            "user_id",
            "total_number",
            "group_challenge_id",
            "video_file",
            "is_updated_file",
        ]


class UpdateUserParticipationStatusInGroupChallengeSerializer(
    serializers.ModelSerializer
):
    """Serializer for update user participation in a group challenge"""

    user_id = serializers.IntegerField(default=None)
    group_challenge_id = serializers.IntegerField(default=None)
    want_to_participate = serializers.BooleanField(default=None)
    challenge_type = serializers.CharField(default="")

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = GroupChallengeModel
        fields = ["user_id", "group_challenge_id", "want_to_participate"]


class GetAllTitlesOfPublicCustomGroupChallengeSerializer(serializers.ModelSerializer):
    """Serializer for getting all participants in group challenge"""

    user_id = serializers.CharField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = PublicCustomGroupChallengesTitleModel
        fields = ["user_id"]
