import django
from django.db import models

from advertisement.models import AdvertisementModel
from user.models import UserModel


class LogsOfPagesOfUserModel(models.Model):
    """Model for logs of handling how many times in a day user went on particular page"""

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, null=True, default=None
    )
    group_challenges_page = models.IntegerField(blank=True, default=0)
    subscriptions_page = models.IntegerField(blank=True, default=0)
    add_commitment_page = models.IntegerField(blank=True, default=0)
    performers_of_the_week_page = models.IntegerField(blank=True, default=0)
    dashboard_page = models.IntegerField(blank=True, default=0)
    otp_page = models.IntegerField(blank=True, default=0)
    individual_user_performance_page = models.IntegerField(blank=True, default=0)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()


class LogsOfUserProgressTapModel(models.Model):
    """Model for logs of handling how many times user visited other user performance portal"""

    id = models.AutoField(primary_key=True)
    from_user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, null=True, default=None
    )
    to_user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        null=True,
        default=None,
        related_name="to_user",
    )
    number_of_times = models.IntegerField(blank=True, default=0)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()


class LogsOfUserTapOnAdvertisementModel(models.Model):
    """Model for logs of handling how many times user tapped on details of advertisement"""

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, null=True, default=None
    )
    advertisement = models.ForeignKey(
        AdvertisementModel, on_delete=models.CASCADE, null=True, default=None
    )
    number_of_times = models.IntegerField(blank=True, default=0)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    objects = models.Manager()
