from django.db import models
import django

# Create your models here.
class ChallengesResultModel(models.Model):
    """Model for challenges result data"""
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(blank=True,default=0)
    competition_id = models.IntegerField(blank=True,default=0)
    rank = models.IntegerField(blank=True,default=0)
    prize_money = models.IntegerField(blank=True,default=0)
    description = models.CharField(max_length=200,blank=False,default='')
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()


