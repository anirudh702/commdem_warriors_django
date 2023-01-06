from django.contrib import admin
from challenges.models import WorkoutLevelModel, WorkoutWiseChallengesModel

# Register your models here.
@admin.register(WorkoutLevelModel)
class ExerciseLevelModelAdmin(admin.ModelAdmin):
    pass

@admin.register(WorkoutWiseChallengesModel)
class ExerciseWiseChallengesModelAdmin(admin.ModelAdmin):
    pass
