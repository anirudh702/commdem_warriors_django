from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import django

from designation.models import DesignationModel
from income.models import IncomeModel

# Create your models here.
class UserModel(models.Model):
    """Model for user data"""
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100,blank=False)
    mobile_number = PhoneNumberField(null=False, blank=False,unique=True,db_index=True,error_messages ={
                    "unique":"This mobile number already exists in our database"
                    })
    email = models.EmailField(max_length = 254,blank=True,null=True,unique=True,db_index=True,error_messages ={
                    "unique":"This Email already exists in our database"
                    })
    profile_pic = models.FileField(blank=True)
    birth_date = models.DateField(blank=False,default=django.utils.timezone.now)
    password = models.CharField(max_length=50,blank=True,default='')
    is_subscribed = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    joining_date = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_active = models.BooleanField(default=False)
    objects = models.Manager()

    # class Meta:
    #     managed = False
    #     db_table='user_usermodel'

class UserPaymentDetailsModel(models.Model):
    """Model for user payment details"""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True)
    payment_id = models.CharField(max_length=50)
    # subscription = models.ForeignKey('subscription.SubscriptionModel', on_delete=models.CASCADE,null=True)
    subscription_id=models.IntegerField(blank=True,default=0)
    date_of_payment = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_active = models.BooleanField(default=False)
    objects = models.Manager()

class UserSubscriptionDetailsModel(models.Model):
    """Model for user subscription details"""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True)
    # subscription = models.ForeignKey('subscription.SubscriptionModel', on_delete=models.CASCADE,null=True)
    subscription_id=models.IntegerField(blank=True,default=0)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_active = models.BooleanField(default=False)
    objects = models.Manager()

class UserGoogleSignInModel(models.Model):
    """Model for user google sign in"""
    id = models.AutoField(primary_key=True)
    gmail_id = models.EmailField(max_length = 254)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True)
    uid = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_active = models.BooleanField(default=False)
    objects = models.Manager()

class UserLocationDetailsModel(models.Model):
    """Model for storing user city,state and country"""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True)
    # state = models.ForeignKey(StatesModel, on_delete=models.CASCADE,null=True)
    state_id=models.IntegerField(blank=True,default=0)
    # city = models.ForeignKey(CitiesModel, on_delete=models.CASCADE,null=True)
    city_id=models.IntegerField(blank=True,default=0)
    city_name = models.CharField(max_length=200,default="")
    # country = models.ForeignKey(CountriesModel, on_delete=models.CASCADE,null=True)
    country_id=models.IntegerField(blank=True,default=0)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_active = models.BooleanField(default=False)
    objects = models.Manager()

class UserProfessionalDetailsModel(models.Model):
    """Model for storing user professional details"""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True)
    designation_title = models.CharField(max_length=50,null=False,blank=False,default="")
    designation = models.ForeignKey(DesignationModel, on_delete=models.CASCADE,null=True)
    # designation_id=models.IntegerField(blank=True,default=0)
    income_range = models.ForeignKey(IncomeModel, on_delete=models.CASCADE,null=True)
    # income_range_id=models.IntegerField(blank=True,default=0)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_active = models.BooleanField(default=False)
    objects = models.Manager()

class UserHealthDetailsModel(models.Model):
    """Model for storing user health details"""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True)
    weight = models.FloatField(blank=True,default=0.0)
    height = models.IntegerField(blank=True,default=0)
    gender = models.CharField(max_length=30,blank=False)
    age = models.BigIntegerField(blank=False)
    is_medicine_ongoing = models.BooleanField(default=False)
    any_health_issues = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_active = models.BooleanField(default=False)
    objects = models.Manager()

class keysToUpdateInFrontEndModel(models.Model):
    """Model for storing update of database in frontend"""
    id = models.AutoField(primary_key=True)
    is_new_commitment_category_added = models.BooleanField(default=False)
    is_commitment_table_updated = models.BooleanField(default=False)
    objects = models.Manager()
