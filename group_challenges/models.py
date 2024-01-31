import django
from django.db import models

from commitment.models import CommitmentNameModel
from subscription.models import SubscriptionModel
from user.models import UserModel


class WorkoutSuggestionsForGroupChallengeModel(models.Model):
    """Model for storing suggestions of workout for a group challenge"""

    id = models.AutoField(primary_key=True)
    workout_name = models.ForeignKey(
        CommitmentNameModel, on_delete=models.CASCADE, null=True, default=None
    )
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.workout_name


class GroupChallengeTypeModel(models.Model):
    """Model for storing type of a group challenge"""

    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=80, blank=False, unique=False, db_index=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.type


class PublicCustomGroupChallengesTitleModel(models.Model):
    """Model for titles of public custom challenges which subscribed user can conduct and it is open for all users"""

    id = models.AutoField(primary_key=True)
    challenge_video_url = models.CharField(
        max_length=80, blank=True, unique=False, db_index=True
    )
    challenge_title = models.CharField(max_length=80, db_index=True, default="")
    challenge_image = models.FileField(blank=True)
    suggested_workout = models.ManyToManyField(CommitmentNameModel, blank=True)
    is_limited_time_challenge = models.BooleanField(default=False)
    time_in_seconds = models.IntegerField(blank=False, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()


# Create your models here.
class GroupChallengeModel(models.Model):
    """Model for handling all types of group challenges"""

    id = models.AutoField(primary_key=True)
    challenge_type = models.ForeignKey(
        GroupChallengeTypeModel, on_delete=models.CASCADE, null=True, blank=True
    )
    challenge_name = models.CharField(
        max_length=80, blank=False, unique=False, db_index=True
    )
    challenge_video_url = models.CharField(
        max_length=80, blank=True, unique=False, db_index=True
    )
    challenge_title = models.CharField(max_length=80, db_index=True, default="")
    challenge_image = models.FileField(blank=True)
    suggested_workout = models.ManyToManyField(CommitmentNameModel, blank=True)
    time_in_seconds = models.IntegerField(blank=False, default=0)
    is_limited_time_challenge = models.BooleanField(default=False)
    challenge_date = models.DateField(blank=True, null=True)
    max_participants_allowed = models.CharField(max_length=10, blank=True, default="")
    price_to_pay = models.CharField(max_length=10, blank=True, default="")
    subscription = models.ForeignKey(
        SubscriptionModel, on_delete=models.CASCADE, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()


class ParticipantsInGroupChallengesModel(models.Model):
    """Model for participants information in all types of group challenges"""

    id = models.AutoField(primary_key=True)
    challenge_type = models.ForeignKey(
        GroupChallengeTypeModel, on_delete=models.CASCADE, null=True, blank=True
    )
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, null=True, default=None
    )
    group_challenge = models.ForeignKey(
        GroupChallengeModel, on_delete=models.CASCADE, null=True, default=None
    )
    challenge_video = models.FileField(blank=True)
    has_submitted_video = models.BooleanField(default=False)
    hide_from_user = models.BooleanField(default=False)
    date_of_submission = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()


class GroupChallengesPaymentModel(models.Model):
    """Model for handling payment for all types of group challenges created by user"""

    id = models.AutoField(primary_key=True)
    challenge_type = models.ForeignKey(
        GroupChallengeTypeModel, on_delete=models.CASCADE, null=True, blank=True
    )
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True)
    payment_id = models.CharField(max_length=50)
    group_challenge = models.ForeignKey(
        GroupChallengeModel, on_delete=models.CASCADE, null=True
    )
    date_of_payment = models.DateTimeField(
        default=django.utils.timezone.now, blank=True
    )
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()


class RulesOfGroupChallengeModel(models.Model):
    """Model for rules of group challenge"""

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, db_index=True, default="")
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()


class GuidelinesOfGroupChallengeModel(models.Model):
    """Model for guidelines of all types of group challenge"""

    id = models.AutoField(primary_key=True)
    challenge_id = models.IntegerField(blank=False, default=0)
    title = models.CharField(max_length=100, db_index=True, default="")
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()
