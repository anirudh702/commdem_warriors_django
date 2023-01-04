from django.contrib import admin
from challenges.models import ExerciseLevelModel, ExerciseWiseChallengesModel

# Register your models here.
@admin.register(ExerciseLevelModel)
class ExerciseLevelModelAdmin(admin.ModelAdmin):
    pass

@admin.register(ExerciseWiseChallengesModel)
class ExerciseWiseChallengesModelAdmin(admin.ModelAdmin):
    pass
