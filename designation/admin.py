from django.contrib import admin

from designation.models import DesignationModel


# Register your models here.
@admin.register(DesignationModel)
class DesignationModelAdmin(admin.ModelAdmin):
    pass
