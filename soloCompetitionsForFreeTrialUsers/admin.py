from django.contrib import admin

from soloCompetitionsForFreeTrialUsers.models import FreeTrialSoloChallengesModel, RulesOfSoloChallengesModel

# Register your models here.
@admin.register(FreeTrialSoloChallengesModel)
class FreeTrialSoloChallengesModelAdmin(admin.ModelAdmin):
    pass

@admin.register(RulesOfSoloChallengesModel)
class RulesOfSoloChallengesModelAdmin(admin.ModelAdmin):
    pass
