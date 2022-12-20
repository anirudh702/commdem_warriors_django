import django
from django.db import models
from commitment.models import CommitmentModel

from user.models import UserModel

# Create your models here.
class voiceAssistantLanguagesModel(models.Model):
    id = models.AutoField(primary_key=True)
    languageName = models.CharField(max_length=30,blank=False)
    languageCode = models.CharField(max_length=5,blank=False)
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

class userCommitmentVoiceBeforeUpdateModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE,null=True)
    commitment = models.ForeignKey(CommitmentModel, on_delete=models.CASCADE,null=True)
    audio_file_path = models.FileField(blank=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_active = models.BooleanField(default=True)
    objects = models.Manager()
