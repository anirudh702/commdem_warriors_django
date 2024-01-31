from django.contrib import admin

from challenges_result.models import ChallengesResultModel


# Register your models here.
@admin.register(ChallengesResultModel)
class ChallengesResultModelAdmin(admin.ModelAdmin):
    pass
