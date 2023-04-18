import django
from django.db import models
from django.contrib.postgres.fields import ArrayField
from user.models import UserModel

# Create your models here.

class GroupChatModel(models.Model):
    """Model for group chat module"""
    id = models.AutoField(primary_key=True)
    from_user = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True,related_name='from_user_detail')
    chat_message = models.CharField(max_length=2000,blank=True,default='')
    Files = ArrayField(base_field=models.FileField(blank=True),default=list, blank=True,null=True)
    is_message_seen_by_all = models.BooleanField(default=False)
    is_first_message_of_day = models.BooleanField(default=False)
    files_path = ArrayField(base_field=models.CharField(max_length=100,null=True),default=list, blank=True,null=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()
