import django
from django.db import models

from commitment.models import CommitmentNameModel


# Create your models here.
class WorkoutLevelModel(models.Model):
    """Model for level of workout data"""

    id = models.AutoField(primary_key=True)
    level_name = models.CharField(
        max_length=20, blank=False, unique=True, db_index=True
    )
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.level_name


class WorkoutModel(models.Model):
    """Model for workout level wise"""

    id = models.AutoField(primary_key=True)
    level_of_workout = models.ForeignKey(
        WorkoutLevelModel, on_delete=models.CASCADE, null=False
    )
    workout_name = models.ForeignKey(
        CommitmentNameModel, on_delete=models.CASCADE, null=False
    )
    workout_video_url = models.CharField(
        max_length=80, blank=False, unique=True, db_index=True
    )
    workout_title = models.CharField(max_length=80, db_index=True, default="")
    workout_image = models.FileField(blank=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.workout_title
