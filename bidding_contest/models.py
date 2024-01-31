import django
from django.db import models

from group_challenges.models import GroupChallengeModel
from user.models import UserModel


class BiddingContestModel(models.Model):
    """Model for bidding contest for particular fitness challenge"""

    id = models.AutoField(primary_key=True)
    group_challenge = models.ForeignKey(
        GroupChallengeModel, on_delete=models.CASCADE, null=True, default=None
    )
    bid_price = models.IntegerField(blank=False, default=0)
    max_bids_allowed = models.IntegerField(blank=False, default=0)
    bids_placed = models.IntegerField(blank=False, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.group_challenge.challenge_name


class ParticipantsInBiddingContestModel(models.Model):
    """Model for participants information in bidding contest"""

    id = models.AutoField(primary_key=True)
    bidding_contest = models.ForeignKey(
        BiddingContestModel, on_delete=models.CASCADE, null=True, blank=True
    )
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, null=True, default=None
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()


class BiddingContestPaymentModel(models.Model):
    """Model for handling payment made by user in a bidding contest"""

    id = models.AutoField(primary_key=True)
    bidding_contest = models.ForeignKey(
        BiddingContestModel, on_delete=models.CASCADE, null=True, blank=True
    )
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True)
    payment_id = models.CharField(max_length=50)
    date_of_payment = models.DateTimeField(
        default=django.utils.timezone.now, blank=True
    )
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()


class QuestionsForBiddingContestModel(models.Model):
    """Model for asking questions to a customer in a bidding contest"""

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300)
    bidding_contest = models.ForeignKey(
        BiddingContestModel, on_delete=models.CASCADE, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()


class AnswersOfBiddingContestModel(models.Model):
    """Model for storing answers of customers in a bidding contest"""

    id = models.AutoField(primary_key=True)
    answer = models.CharField(max_length=100)
    bidding_contest = models.ForeignKey(
        BiddingContestModel, on_delete=models.CASCADE, null=True, blank=True
    )
    question = models.ForeignKey(
        QuestionsForBiddingContestModel,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()


class BiddingContestResultModel(models.Model):
    """Model for bidding contest result data"""

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, null=True, default=None
    )
    bidding_contest = models.ForeignKey(
        BiddingContestModel, on_delete=models.CASCADE, null=True, default=None
    )
    rank = models.IntegerField(blank=True, default=0)
    prize_money = models.IntegerField(blank=True, default=0)
    description = models.CharField(max_length=200, blank=False, default="")
    is_payment_done = models.BooleanField(default=False)
    payment_transaction_id = models.CharField(max_length=100, blank=True, default="")
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()
