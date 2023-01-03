from django.contrib import admin

from referralCode.models import ReferralCodeModel

# Register your models here.
@admin.register(ReferralCodeModel)
class ReferralCodeModelAdmin(admin.ModelAdmin):
    pass