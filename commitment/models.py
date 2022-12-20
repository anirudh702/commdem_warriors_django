from datetime import *
from enum import unique
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import django
from django.contrib.postgres.fields import ArrayField

from user.models import UserModel

def next_day_datetime():
    """Function for returning next day datetime while user adds new commitment"""
    return datetime.now() + timedelta(days=1)

# Create your models here.

class CommitmentCategoryModel(models.Model):
    """Model for commitment category data"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200,null=False,unique=True,db_index=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()

    def __str__(self):
         return self.name

class CommitmentNameModel(models.Model):
    """Model for commitment name data"""
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(CommitmentCategoryModel, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=200,null=False,unique=True,db_index=True)
    successName = models.CharField(max_length=200,null=False,unique=True,db_index=True)
    failureName = models.CharField(max_length=200,null=False,unique=True,db_index=True)
    currentDayName = models.CharField(max_length=200,null=False,unique=True,db_index=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()
    def __str__(self):
         return self.name

class CauseOfCategorySuccessOrFailureModel(models.Model):
    """Model for cause of category success/failure data"""
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(CommitmentCategoryModel, on_delete=models.CASCADE,null=False)
    title = models.CharField(max_length=200,null=False,unique=True,db_index=True)
    is_success = models.BooleanField(null=False)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()
    def __str__(self):
         return self.title

class CommitmentModel(models.Model):
    """Model for commitment data"""
    id = models.AutoField(primary_key=True)
    # user = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True,default=None)
    user_id=models.IntegerField(blank=True,default=0)
    category = models.ForeignKey(CommitmentCategoryModel, on_delete=models.CASCADE,null=True)
    commitment_name = models.ForeignKey(CommitmentNameModel, on_delete=models.CASCADE,null=True)
    commitment_date = models.DateTimeField(default=next_day_datetime, blank=True)
    is_done = models.BooleanField(default=False)
    is_updated = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()
    # def __str__(self):
    #      return self.commitment_name

class ReasonBehindCommitmentSuccessOrFailureForUser(models.Model):
    """Model for storing reasons behind success or failure of a particular commitment of a user"""
    id = models.AutoField(primary_key=True)
    # user = models.ForeignKey('user.UserModel', on_delete=models.CASCADE,null=False,default=None)
    user_id=models.IntegerField(blank=True,default=0)
    commitment = models.ForeignKey(CommitmentModel, on_delete=models.CASCADE,null=False)
    cause_of_category_success_or_failure = models.ForeignKey(CauseOfCategorySuccessOrFailureModel, on_delete=models.CASCADE,null=False)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()
    def __str__(self):
         return self.cause_of_category_success_or_failure__title


class CommitmentGraphDataModel(models.Model):
    """Model for commitment graph data"""
    id = models.AutoField(primary_key=True)
    # user = models.ForeignKey('user.UserModel', on_delete=models.CASCADE,null=True,default=None)
    user_id=models.IntegerField(blank=True,default=0)
    percentage_done = models.FloatField()
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()
