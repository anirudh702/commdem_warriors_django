from django.db import models
import django

class GroupChallengesPaymentStatusModel(models.Model):
    """Model for displaying group challenges payment status"""
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=50,blank=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()

# Create your models here.
class ChallengesResultModel(models.Model):
    """Model for challenges result data"""
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(blank=True,default=0)
    competition_id = models.IntegerField(blank=True,default=0)
    rank = models.IntegerField(blank=True,default=0)
    prize_money = models.IntegerField(blank=True,default=0)
    description = models.CharField(max_length=200,blank=False,default='')
    payment_status = models.ForeignKey(GroupChallengesPaymentStatusModel, on_delete=models.CASCADE,null=True)
    is_min_percentage_achieved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()
