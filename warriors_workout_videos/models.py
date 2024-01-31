import django
from django.db import models

from commitment.models import CommitmentModel
from user.models import UserModel


# Create your models here.
class WarriorsWorkoutVideosModel(models.Model):
    """Model for warriors workout data"""

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True)
    commitment = models.ForeignKey(
        CommitmentModel, on_delete=models.CASCADE, null=False
    )
    description = models.CharField(max_length=200, blank=True, null=True)
    workout_file = models.FileField(blank=True, null=True)
    workout_thumbnail_file = models.FileField(blank=True, null=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_private_for_all = models.BooleanField(default=False, blank=True, null=True)
    private_for_this_gender = models.CharField(
        max_length=10, blank=True, null=True, default=""
    )
    objects = models.Manager()


class UserWiseWorkoutVideosPrivacyModel(models.Model):
    """Model for user wise workout videos privacy"""

    id = models.AutoField(primary_key=True)
    fromUser = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, null=True, related_name="from_user"
    )
    toUser = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True)
    workoutVideo = models.ForeignKey(
        WarriorsWorkoutVideosModel, on_delete=models.CASCADE, null=False
    )
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_private = models.BooleanField(default=False)
    objects = models.Manager()
