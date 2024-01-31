import django
from django.db import models


class TypeOfFoodModel(models.Model):
    """Model for type of food data (breakfast,snacks, lunch or dinner)"""

    id = models.AutoField(primary_key=True)
    type_of_food_name = models.CharField(max_length=40, blank=False)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()


# Create your models here.
class FoodModel(models.Model):
    """Model for food data"""

    id = models.AutoField(primary_key=True)
    food_name = models.CharField(max_length=100, blank=False)
    food_image = models.FileField(blank=True)
    type_of_food = models.ForeignKey(
        TypeOfFoodModel, on_delete=models.CASCADE, null=True
    )
    is_for_weight_loss = models.BooleanField(default=False)
    is_veg = models.BooleanField(default=False)
    youtube_url = models.CharField(max_length=50, blank=True, default="")
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()
