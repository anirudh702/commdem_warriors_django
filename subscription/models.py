from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import django

# Create your models here.
class SubscriptionModel(models.Model):
    """Model for subscription data"""
    id = models.AutoField(primary_key=True)
    amount_in_dollars = models.BigIntegerField()
    duration_in_months = models.CharField(max_length=100,blank=False,unique=False)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()
