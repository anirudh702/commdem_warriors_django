from django.contrib import admin

from advertisement.models import AdvertisementModel


# Register your models here.
@admin.register(AdvertisementModel)
class AdvertisementModelAdmin(admin.ModelAdmin):
    pass
