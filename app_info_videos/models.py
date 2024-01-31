import django
from django.db import models


# Create your models here.
class AppInfoVideosModel(models.Model):
    """Model for challenges result data"""

    id = models.AutoField(primary_key=True)
    video_url = models.CharField(max_length=20, blank=True)
    title = models.CharField(max_length=100, blank=True, unique=False)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()
