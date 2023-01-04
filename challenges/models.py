# from django.db import models
# import django

# # Create your models here.
# class ChallengesModel(models.Model):
#     """Model for challenges data"""
#     id = models.AutoField(primary_key=True)
#     exercise = models.ForeignKey(ExerciseModel, on_delete=models.CASCADE,null=True)
#     challenge_title = models.CharField(max_length=100)
#     full_demo_video_url = models.CharField(max_length=50)
#     single_exercise_video_url = models.CharField(max_length=50)
#     main_thumbnail_image = models.CharField(max_length=50)
#     full_video_thumbnail_image = models.CharField(max_length=50)
#     single_exercise_thumbnail_image = models.CharField(max_length=50)
#     warm_up_exercise_video = models.CharField(max_length=50)
#     cool_down_exercise_video = models.CharField(max_length=50)
#     what_to_do_before_exercise = models.CharField(max_length=50)
#     what_not_to_do_before_exercise = models.CharField(max_length=50)
#     what_to_do_after_exercise = models.CharField(max_length=50)
#     what_not_to_do_after_exercise = models.CharField(max_length=50)
#     is_group_challenge = models.BooleanField(default=False)
#     created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
#     updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
#     objects = models.Manager()


from django.db import models
import django

from commitment.models import CommitmentNameModel

# Create your models here.
class ExerciseLevelModel(models.Model):
    """Model for level of exercise data"""
    id = models.AutoField(primary_key=True)
    level_name = models.CharField(max_length=20,blank=False,unique=True,db_index=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()
    def __str__(self):
         return self.level_name

class ExerciseWiseChallengesModel(models.Model):
    """Model for challenges for every exercise workout level wise"""
    id = models.AutoField(primary_key=True)
    level_of_exercise = models.ForeignKey(ExerciseLevelModel, on_delete=models.CASCADE,null=False)
    exercise = models.ForeignKey(CommitmentNameModel, on_delete=models.CASCADE,null=False)
    challenge_name = models.CharField(max_length=80,blank=False,unique=True,db_index=True)
    challenge_image = models.FileField(blank=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()
    def __str__(self):
         return self.challenge_name