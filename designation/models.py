import django
from django.db import models


# Create your models here.
class DesignationModel(models.Model):
    """Model for designation data"""

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=False, unique=True, db_index=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.title
