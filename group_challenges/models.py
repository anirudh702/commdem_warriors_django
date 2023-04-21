import django
from django.db import models
from commitment.models import CommitmentNameModel

from user.models import UserModel

class WorkoutSuggestionsForGroupChallengeModel(models.Model):
    """Model for storing suggestions of workout for a group challenge"""
    id = models.AutoField(primary_key=True)
    workout_name = models.ForeignKey(CommitmentNameModel, on_delete=models.CASCADE,null=True,default=None)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.workout_name

# Create your models here.
class GroupChallengesModel(models.Model):
    """Model for group challenges"""
    id = models.AutoField(primary_key=True)
    challenge_name = models.CharField(max_length=80,blank=False,unique=True,db_index=True)
    challenge_video_url = models.CharField(max_length=80,blank=False,unique=True,db_index=True)
    challenge_title = models.CharField(max_length=80,db_index=True,default='')
    challenge_image = models.FileField(blank=True)
    suggested_workout = models.ManyToManyField(CommitmentNameModel)
    min_age=models.IntegerField(blank=True,default=0)
    max_age=models.IntegerField(blank=True,default=0)
    min_rating=models.IntegerField(blank=True,default=0)
    max_rating=models.IntegerField(blank=True,default=0)
    gender = models.CharField(max_length=10,blank=False,default='male')
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()

class ParticipantsInGroupChallengeModel(models.Model):
    """Model for participants information in group challenge"""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True,default=None)
    group_challenge = models.ForeignKey(GroupChallengesModel, on_delete=models.CASCADE,null=True,default=None)
    challenge_video = models.FileField(blank=True)
    has_submitted_video = models.BooleanField(default=False)
    hide_from_user = models.BooleanField(default=False)
    date_of_submission = models.DateTimeField(blank=True,null=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()

class RulesOfGroupChallengeModel(models.Model):
    """Model for rules of group challenge"""
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100,db_index=True,default='')
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()

class GuidelinesOfGroupChallengeModel(models.Model):
    """Model for guidelines of group challenge"""
    id = models.AutoField(primary_key=True)
    group_challenge = models.ForeignKey(GroupChallengesModel, on_delete=models.CASCADE,null=True,default=None)
    title = models.CharField(max_length=100,db_index=True,default='')
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()