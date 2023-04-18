from django.db import models
import django

from user.models import UserModel

# Create your models here.
class PositiveAffirmationModel(models.Model):
    """Model for storing positive affirmations"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200,null=False,db_index=True,default='',unique=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()

class UserAffirmationModel(models.Model):
    """Model for updating if user spoke positive affirmation"""
    id = models.AutoField(primary_key=True)
    number_of_commitment_for_week_id = models.IntegerField(blank=True,default=0,unique=False)
    user_id = models.IntegerField(blank=True,default=0,unique=False)
    did_user_speak = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()