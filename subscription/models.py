from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import django


class SubscriptionLevelModel(models.Model):
    """Model for subscription level data"""
    id = models.AutoField(primary_key=True)
    level = models.CharField(max_length=30,default="")
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()

# Create your models here.
class SubscriptionModel(models.Model):
    """Model for subscription data"""
    id = models.AutoField(primary_key=True)
    amount = models.BigIntegerField()
    level_name = models.ForeignKey(SubscriptionLevelModel, on_delete=models.CASCADE,blank=True,null=True)
    designation_id=models.IntegerField(blank=True,default=0,null=True)
    refund_amount=models.IntegerField(blank=True,default=0,null=True)
    is_free_trial = models.BooleanField(default=False)
    is_call_service_included = models.BooleanField(default=False)
    duration = models.CharField(max_length=100,blank=True,unique=False)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_active = models.BooleanField(default=True)
    objects = models.Manager()
    class Meta:
        app_label = 'subscription'
    # def __str__(self):
    #      return self.commitment_name
