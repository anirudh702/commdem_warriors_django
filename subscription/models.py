from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import django

# Create your models here.
class SubscriptionModel(models.Model):
    """Model for subscription data"""
    id = models.AutoField(primary_key=True)
    amount = models.BigIntegerField()
    designation_id=models.IntegerField(blank=True,default=0)
    is_free_trial = models.BooleanField(default=False)
    duration = models.CharField(max_length=100,blank=True,unique=False)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()
    class Meta:
        app_label = 'subscription'

