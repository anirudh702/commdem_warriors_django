from django.contrib import admin

from location.models import CitiesModel


# Register your models here.
@admin.register(CitiesModel)
class LocationCitiesModelAdmin(admin.ModelAdmin):
    pass
