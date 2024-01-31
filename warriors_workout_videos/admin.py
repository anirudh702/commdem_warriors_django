from django.contrib import admin

from warriors_workout_videos.models import WarriorsWorkoutVideosModel


# Register your models here.
@admin.register(WarriorsWorkoutVideosModel)
class WarriorsWorkoutVideosModelAdmin(admin.ModelAdmin):
    pass
