from django.contrib import admin

from referralCode.models import ReferralCodeModel
from user.models import ReferralPaymentStatusModel


# Register your models here.
@admin.register(ReferralCodeModel)
class ReferralCodeModelAdmin(admin.ModelAdmin):
    pass


@admin.register(ReferralPaymentStatusModel)
class ReferralPaymentStatusModelAdmin(admin.ModelAdmin):
    pass
