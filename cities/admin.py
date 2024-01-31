from django.contrib import admin

from cities.models import CitiesModel


# Register your models here.
@admin.register(CitiesModel)
class CitiesModelAdmin(admin.ModelAdmin):
    pass
