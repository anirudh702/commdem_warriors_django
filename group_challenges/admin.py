from django.contrib import admin

from group_challenges.models import GroupChallengesModel, ParticipantsInGroupChallengeModel

# Register your models here.
@admin.register(GroupChallengesModel)
class GroupChallengesModelAdmin(admin.ModelAdmin):
    pass

@admin.register(ParticipantsInGroupChallengeModel)
class ParticipantsInGroupChallengeModelAdmin(admin.ModelAdmin):
    pass