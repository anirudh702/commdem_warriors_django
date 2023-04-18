from django.contrib import admin
from subscription.models import SubscriptionLevelModel, SubscriptionModel

# Register your models here.
@admin.register(SubscriptionModel)
class SubscriptionModelAdmin(admin.ModelAdmin):
    list_filter = (
        ('is_active'),
    )
    pass

@admin.register(SubscriptionLevelModel)
class SubscriptionLevelModelAdmin(admin.ModelAdmin):
    pass
