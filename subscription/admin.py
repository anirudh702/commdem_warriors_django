from django.contrib import admin
from subscription.models import SubscriptionModel

# Register your models here.
@admin.register(SubscriptionModel)
class SubscriptionModelAdmin(admin.ModelAdmin):
    pass
