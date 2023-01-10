from datetime import *
from enum import unique
from django.db import models
import django

from commitment.models import next_day_datetime

# Create your models here.

class ChallengesModel(models.Model):
    """Model for challenges model"""
    id = models.AutoField(primary_key=True)
    challenge_name = models.CharField(max_length=80,blank=False,unique=True,db_index=True)
    challenge_video_url = models.CharField(max_length=80,blank=False,unique=True,db_index=True)
    challenge_title = models.CharField(max_length=80,db_index=True,default='')
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()

    def __str__(self):
         return self.name
