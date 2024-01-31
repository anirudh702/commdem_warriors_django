import django
from django.db import models


# Create your models here.
class mcqsChoicesModel(models.Model):
    """Model for storing mcqs data"""

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, default="")
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_active = models.BooleanField(default=True)
    objects = models.Manager()


class QuestionsToAskBeforeModel(models.Model):
    """Model for storing questions data to ask befoe a relationship"""

    id = models.AutoField(primary_key=True)
    main_question = models.CharField(max_length=200, default="")
    mcqs = models.ManyToManyField(mcqsChoicesModel)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()
