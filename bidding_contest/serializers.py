"""Serializer for user module"""

from rest_framework import serializers

from bidding_contest.models import BiddingContestModel, BiddingContestPaymentModel


class GetBiddingContestSerializer(serializers.ModelSerializer):
    """Serializer for getting bidding contest details"""

    user_id = serializers.IntegerField(default=None)
    challenge_id = serializers.IntegerField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = BiddingContestModel
        fields = ["user_id", "challenge_id"]


class AddNewParticipantSerializer(serializers.ModelSerializer):
    """Serializer for adding new participant in bidding contest"""

    user_id = serializers.IntegerField(default=None)
    payment_id = serializers.CharField(default=None)
    answers = serializers.ListField(default=None)
    date_of_payment = serializers.CharField(default=None)
    bidding_contest_id = serializers.IntegerField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = BiddingContestPaymentModel
        fields = [
            "user_id",
            "payment_id",
            "bidding_contest_id",
            "date_of_payment",
            "answers",
        ]


class UpdateParticipantDetailsSerializer(serializers.ModelSerializer):
    """Serializer for updating participant details in bidding contest"""

    user_id = serializers.IntegerField(default=None)
    answers = serializers.ListField(default=None)
    bidding_contest_id = serializers.IntegerField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = BiddingContestPaymentModel
        fields = ["user_id", "bidding_contest_id", "answers"]
