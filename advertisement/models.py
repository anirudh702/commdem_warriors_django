from django.db import models
import django
from datetime import *
from user.models import UserModel

def next_day_datetime(days):
    """Function for returning next day datetime while user adds new commitment"""
    return datetime.now() + timedelta(days=days)

# Create your models here.
class AdvertisementModel(models.Model):
    """Model for advertisement data"""
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100,blank=False)
    description = models.CharField(max_length=300,blank=False)
    image_url = models.FileField(blank=True)
    video_url = models.FileField(blank=True)
    ad_type = models.CharField(max_length=30,blank=False)
    start_date = models.DateField(blank=True,default=next_day_datetime(1))
    end_date = models.DateField(blank=True,default=next_day_datetime(7))
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    status = models.BooleanField(default=False)
    objects = models.Manager()


class AdvertiserModel(models.Model):
    """Model for advertiser details"""
    id = models.AutoField(primary_key=True)
    advertisement = models.ForeignKey(AdvertisementModel, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_active = models.BooleanField(default=False)
    objects = models.Manager()

class AdvertisementClicksModel(models.Model):
    """Model for clicks on advertisement details"""
    id = models.AutoField(primary_key=True)
    advertisement = models.ForeignKey(AdvertisementModel, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True)
    click_date = models.DateTimeField(default=django.utils.timezone.now, blank=False)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_active = models.BooleanField(default=False)
    objects = models.Manager()

class AdvertisementViewsModel(models.Model):
    """Model for views on advertisement details"""
    id = models.AutoField(primary_key=True)
    advertisement = models.ForeignKey(AdvertisementModel, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True)
    view_date = models.DateTimeField(default=django.utils.timezone.now, blank=False)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_active = models.BooleanField(default=False)
    objects = models.Manager()