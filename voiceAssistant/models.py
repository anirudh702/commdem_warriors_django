import django
from django.db import models

from commitment.models import (
    CauseOfCategorySuccessOrFailureModel,
    CommitmentCategoryModel,
    CommitmentModel,
)
from designation.models import DesignationModel
from user.models import UserModel


# Create your models here.
class voiceAssistantLanguagesModel(models.Model):
    id = models.AutoField(primary_key=True)
    languageName = models.CharField(max_length=30, blank=False)
    languageCode = models.CharField(max_length=5, blank=False)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()


class userPreferredVoiceLanguageModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True)
    voice_assistant_language = models.ForeignKey(
        voiceAssistantLanguagesModel, on_delete=models.CASCADE, null=True
    )
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()


class userCommitmentVoiceBeforeUpdateModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True)
    commitment = models.ForeignKey(CommitmentModel, on_delete=models.CASCADE, null=True)
    audio_file_path = models.FileField(blank=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_active = models.BooleanField(default=True)
    objects = models.Manager()


class voiceAssistantAfterUpdateMessageModel(models.Model):
    id = models.AutoField(primary_key=True)
    commitment_category = models.ForeignKey(
        CommitmentCategoryModel, on_delete=models.CASCADE, null=True
    )
    reason_behind_commitment_success_or_failure = models.ForeignKey(
        CauseOfCategorySuccessOrFailureModel, on_delete=models.CASCADE, null=True
    )
    # range_of_success_of_exercise_in_this_week = models.CharField(max_length=100,blank=True)
    voice_assistant_message = models.CharField(max_length=400, blank=False)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.voice_assistant_message

    # def __str__(self):
    #      return self.commitment_name__id
    # def __str__(self):
    #      return self.reason_behind_commitment_success_or_failure__id


class voiceAssistantBeforeUpdateMessageModel(models.Model):
    id = models.AutoField(primary_key=True)
    commitment_category = models.ForeignKey(
        CommitmentCategoryModel, on_delete=models.CASCADE, null=True
    )
    occupation = models.ForeignKey(
        DesignationModel, on_delete=models.CASCADE, null=True
    )
    age_group = models.CharField(max_length=100, blank=True)
    no_of_times_in_current_week = models.IntegerField(blank=True, default=0)
    range_of_success_of_commitment_name_in_this_week = models.CharField(
        max_length=100, blank=True
    )
    is_it_weekend = models.BooleanField(default=True)
    voice_assistant_message = models.CharField(max_length=400, blank=False)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.voice_assistant_message
