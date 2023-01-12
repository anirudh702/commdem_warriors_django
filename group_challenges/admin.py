from django.contrib import admin

from group_challenges.models import GroupChallengesModel, GuidelinesOfGroupChallengeModel, ParticipantsInGroupChallengeModel, RulesOfGroupChallengeModel

# Register your models here.
@admin.register(GroupChallengesModel)
class GroupChallengesModelAdmin(admin.ModelAdmin):
    pass

@admin.register(ParticipantsInGroupChallengeModel)
class ParticipantsInGroupChallengeModelAdmin(admin.ModelAdmin):
    pass

@admin.register(RulesOfGroupChallengeModel)
class RulesOfGroupChallengeModelAdmin(admin.ModelAdmin):
    pass

@admin.register(GuidelinesOfGroupChallengeModel)
class GuidelinesOfGroupChallengeModelAdmin(admin.ModelAdmin):
    pass