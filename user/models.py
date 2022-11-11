from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import django
from designation.models import DesignationModel

from subscription.models import SubscriptionModel

# Create your models here.
class UserModel(models.Model):
    """Model for user data"""
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100,blank=False)
    last_name = models.CharField(max_length=100,blank=False)
    mobile_number = PhoneNumberField(null=False, blank=False)
    profile_pic = models.FileField(blank=True)
    password = models.CharField(max_length=50,null=False)
    age = models.BigIntegerField()
    designation_title = models.CharField(max_length=50,null=False,blank=False,default="")
    designation = models.ForeignKey(DesignationModel, on_delete=models.CASCADE,null=True)
    is_medicine_ongoing = models.BooleanField(default=False)
    any_health_issues = models.BooleanField(default=False)
    is_subscribed = models.BooleanField(default=False)
    joining_date = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()

class UserPaymentDetailsModel(models.Model):
    """Model for user payment details"""
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True)
    payment_id = models.CharField(max_length=50)
    subscription = models.ForeignKey(SubscriptionModel, on_delete=models.CASCADE,null=True)
    date_of_payment = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()

class UserSubscriptionDetailsModel(models.Model):
    """Model for user subscription details"""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True)
    subscription = models.ForeignKey(SubscriptionModel, on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()