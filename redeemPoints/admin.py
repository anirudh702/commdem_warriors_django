from django.contrib import admin

from redeemPoints.models import RedeemPointsModel

# Register your models here.
@admin.register(RedeemPointsModel)
class RedeemPointsModelAdmin(admin.ModelAdmin):
    pass