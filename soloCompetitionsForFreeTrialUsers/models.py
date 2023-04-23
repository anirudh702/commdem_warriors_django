import django
from django.db import models
from commitment.models import CommitmentNameModel
from user.models import UserModel

class WorkoutSuggestionsForSoloChallengeModel(models.Model):
    """Model for storing suggestions of workout for a solo challenge for free trial users"""
    id = models.AutoField(primary_key=True)
    workout_name = models.ForeignKey(CommitmentNameModel, on_delete=models.CASCADE,null=True,default=None)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.workout_name

# Create your models here.
class FreeTrialSoloChallengesModel(models.Model):
    """Model for free trial solo challenges"""
    id = models.AutoField(primary_key=True)
    challenge_name = models.CharField(max_length=80,blank=False,unique=True,db_index=True)
    challenge_video_url = models.CharField(max_length=80,blank=False,unique=True,db_index=True)
    challenge_title = models.CharField(max_length=80,db_index=True,default='')
    challenge_image = models.FileField(blank=True)
    suggested_workout = models.ManyToManyField(CommitmentNameModel)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()

class RulesOfSoloChallengesModel(models.Model):
    """Model for rules of solo challenges for free trial users"""
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100,db_index=True,default='')
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()

class ParticipantsInSoloChallengeModel(models.Model):
    """Model for participants information in solo challenge for free trial users"""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True,default=None,related_name='User')
    solo_challenge = models.ForeignKey(FreeTrialSoloChallengesModel, on_delete=models.CASCADE,null=True,default=None)
    challenge_video = models.FileField(blank=True)
    has_submitted_video = models.BooleanField(default=False)
    hide_from_user = models.BooleanField(default=False)
    date_of_submission = models.DateTimeField(blank=True,null=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()