import django
from django.db import models


# Create your models here.
class RedeemPointsModel(models.Model):
    """Model for redeem Points data"""

    id = models.AutoField(primary_key=True)
    # to_user = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True)
    to_user_id = models.IntegerField(blank=True, default=0)
    from_user_id = models.IntegerField(blank=True, default=0)
    redeem_points = models.BigIntegerField()
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_active = models.BooleanField(default=False)
    objects = models.Manager()
