from datetime import *
from enum import unique
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import django

from user.models import UserModel

def next_day_datetime():
    """Function for returning next day datetime while user adds new commitment"""
    return datetime.now() + timedelta(days=1)

# Create your models here.

class CommitmentCategoryModel(models.Model):
    """Model for commitment category data"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200,null=False,unique=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()

class CommitmentNameModel(models.Model):
    """Model for commitment name data"""
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(CommitmentCategoryModel, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=200,null=False,unique=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()

class CommitmentModel(models.Model):
    """Model for commitment data"""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True)
    category = models.ForeignKey(CommitmentCategoryModel, on_delete=models.CASCADE,null=True)
    commitment_name = models.ForeignKey(CommitmentNameModel, on_delete=models.CASCADE,null=True)
    commitment_date = models.DateTimeField(default=next_day_datetime, blank=True)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()
    

class CommitmentGraphDataModel(models.Model):
    """Model for commitment graph data"""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True)
    percentage_done = models.FloatField()
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()