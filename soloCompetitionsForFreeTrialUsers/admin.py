from django.contrib import admin

from soloCompetitionsForFreeTrialUsers.models import FreeTrialSoloChallengesModel, ParticipantsInSoloChallengeModel, RulesOfSoloChallengesModel

# Register your models here.
@admin.register(FreeTrialSoloChallengesModel)
class FreeTrialSoloChallengesModelAdmin(admin.ModelAdmin):
    pass

@admin.register(RulesOfSoloChallengesModel)
class RulesOfSoloChallengesModelAdmin(admin.ModelAdmin):
    pass

@admin.register(ParticipantsInSoloChallengeModel)
class ParticipantsInSoloChallengeModelAdmin(admin.ModelAdmin):
    pass