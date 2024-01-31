import django
from django.db import models

from group_challenges.models import GroupChallengeModel
from user.models import UserModel


# Create your models here.
class ChallengesResultModel(models.Model):
    """Model for challenges result data"""

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, null=True, default=None
    )
    group_challenge = models.ForeignKey(
        GroupChallengeModel, on_delete=models.CASCADE, null=True, default=None
    )
    rank = models.IntegerField(blank=True, default=0)
    total_done = models.IntegerField(blank=True, default=0)
    prize_money = models.IntegerField(blank=True, default=0)
    description = models.CharField(max_length=200, blank=False, default="")
    is_payment_done = models.BooleanField(default=False)
    payment_transaction_id = models.CharField(max_length=100, blank=True, default="")
    is_min_percentage_achieved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()
