from django.db import models
import django

# Create your models here.
class ReviewModel(models.Model):
    """Model for reviews data"""
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300,blank=True,unique=False)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.title
