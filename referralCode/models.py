import django
from django.db import models


# Create your models here.
class ReferralCodeModel(models.Model):
    """Model for referral code data"""

    id = models.AutoField(primary_key=True)
    # user = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True)
    user_id = models.IntegerField(blank=True, default=0)
    referred_user_phone_number = models.CharField(
        default="", max_length=15, blank=False, unique=False, db_index=True
    )
    referred_user_full_name = models.CharField(
        default="", max_length=50, blank=False, unique=False, db_index=True
    )
    is_payment_done = models.BooleanField(default=False)
    payment_transaction_id = models.CharField(max_length=100, blank=True, default="")
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_active = models.BooleanField(default=False)
    objects = models.Manager()
