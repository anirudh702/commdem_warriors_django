from datetime import *
from enum import unique
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import django
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from positive_affirmations.models import PositiveAffirmationModel
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
    mainTitle = models.CharField(max_length=200,null=False)
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
    # def __str__(self):
    #      return self.title

class   CommitmentModel(models.Model):
    """Model for commitment data"""
    id = models.AutoField(primary_key=True)
    # user = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True,default=None)
    user_id=models.IntegerField(blank=True,default=0)
    total_commitments_done=models.IntegerField(blank=True,default=0)
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
    # def __str__(self):
    #      return self.cause_of_category_success_or_failure__id


class CommitmentGraphDataModel(models.Model):
    """Model for commitment graph data"""
    id = models.AutoField(primary_key=True)
    # user = models.ForeignKey('user.UserModel', on_delete=models.CASCADE,null=True,default=None)
    user_id=models.IntegerField(blank=True,default=0)
    percentage_done = models.FloatField()
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()

class ExerciseModel(models.Model):
    """Model for storing starting time of exercise of a user in a day"""
    id = models.AutoField(primary_key=True)
    user_id=models.IntegerField(blank=True,default=0)
    commitment_name = models.ForeignKey(CommitmentNameModel, on_delete=models.CASCADE,null=False)
    time_to_start = models.CharField(max_length=50,null=False,db_index=True,default='')
    commitment_date = models.DateTimeField(default=next_day_datetime, blank=True)
    did_speak_before = models.BooleanField(default=False)
    did_speak_positive_affirmation = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + timedelta(days_ahead)
    
class UserCommitmentsForNextWeekModel(models.Model):
    """Model for storing minimum number of commitments user wise for next week"""
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(blank=True,default=0,unique=False)
    min_no_of_food_commitments = models.IntegerField(blank=True,default=0,validators=[MinValueValidator(3), MaxValueValidator(7)])
    min_no_of_water_commitments = models.IntegerField(blank=True,default=0,validators=[MinValueValidator(4), MaxValueValidator(7)])
    min_no_of_exercise_commitments = models.IntegerField(blank=True,default=0,validators=[MinValueValidator(3), MaxValueValidator(7)])
    start_date = models.DateField(blank=True,default=next_day_datetime)
    end_date = models.DateField(blank=True,default=next_weekday(datetime.now(), 6))
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()
