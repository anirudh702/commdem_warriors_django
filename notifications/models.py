from django.db import models
import django

from user.models import UserModel

# Create your models here.
class UserPlayerIdModel(models.Model):
    """Model for storing player id of a user"""
    id = models.AutoField(primary_key=True)
    # user = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True)
    user_id=models.IntegerField(blank=True,default=0)
    player_id = models.CharField(max_length=100,blank=False,unique=False,null=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_active = models.BooleanField(default=False)
    objects = models.Manager()
