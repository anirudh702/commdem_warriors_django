from django.contrib import admin
from subscription.models import SubscriptionLevelModel, SubscriptionModel

# Register your models here.
@admin.register(SubscriptionModel)
class SubscriptionModelAdmin(admin.ModelAdmin):
    pass

@admin.register(SubscriptionLevelModel)
class SubscriptionLevelModelAdmin(admin.ModelAdmin):
    pass
