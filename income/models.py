import django
from django.db import models


# Create your models here.
class IncomeModel(models.Model):
    """Model for income data"""

    id = models.AutoField(primary_key=True)
    income_range = models.CharField(max_length=100, blank=False)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()
