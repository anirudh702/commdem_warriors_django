from django.contrib import admin
from workout.models import WorkoutLevelModel, WorkoutModel

# Register your models here.
@admin.register(WorkoutLevelModel)
class ExerciseLevelModelAdmin(admin.ModelAdmin):
    pass

@admin.register(WorkoutModel)
class WorkoutModelAdmin(admin.ModelAdmin):
    pass
