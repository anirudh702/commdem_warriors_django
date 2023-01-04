from django.contrib import admin
from positive_affirmations.models import PositiveAffirmationModel, UserAffirmationModel

# Register your models here.
@admin.register(PositiveAffirmationModel)
class PositiveAffirmationModelAdmin(admin.ModelAdmin):
    pass

@admin.register(UserAffirmationModel)
class UserAffirmationModelAdmin(admin.ModelAdmin):
    pass