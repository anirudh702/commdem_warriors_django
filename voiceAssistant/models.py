import django
from django.db import models

from user.models import UserModel

# Create your models here.
class voiceAssistantLanguagesModel(models.Model):
    id = models.AutoField(primary_key=True)
    language_name = models.CharField(max_length=30,blank=False)
    language_code = models.CharField(max_length=5,blank=False)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()

class userPreferredVoiceLanguageModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True)
    voice_assistant_language = models.ForeignKey(voiceAssistantLanguagesModel, on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()