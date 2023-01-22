import django
from django.db import models
from django.contrib.postgres.fields import ArrayField
from user.models import UserModel

# Create your models here.

class OneToOneChatModel(models.Model):
    """Model for one to one chat module"""
    id = models.AutoField(primary_key=True)
    from_user = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True,related_name='from_user_details')
    to_user = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True)
    chat_message = models.CharField(max_length=1000,blank=True,default='')
    is_message_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()

class OneToOneFilesSharedOnChatModel(models.Model):
    """Model for files shared while one to one conversation in chat"""
    id = models.AutoField(primary_key=True)
    chat = models.ForeignKey(OneToOneChatModel, on_delete=models.CASCADE,null=True)
    path = ArrayField(models.CharField(max_length=100))
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()