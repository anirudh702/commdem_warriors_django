from django.contrib import admin

from group_challenges.models import (
    GroupChallengeModel,
    GroupChallengesPaymentModel,
    GroupChallengeTypeModel,
    ParticipantsInGroupChallengesModel,
    PublicCustomGroupChallengesTitleModel,
)


# Register your models here.
@admin.register(GroupChallengeModel)
class GroupChallengeModelAdmin(admin.ModelAdmin):
    list_filter = ('challenge_type',)


@admin.register(GroupChallengeTypeModel)
class GroupChallengeTypeModelAdmin(admin.ModelAdmin):
    pass


@admin.register(ParticipantsInGroupChallengesModel)
class ParticipantsInGroupChallengesModelAdmin(admin.ModelAdmin):
    pass


@admin.register(GroupChallengesPaymentModel)
class GroupChallengesPaymentModelAdmin(admin.ModelAdmin):
    pass


@admin.register(PublicCustomGroupChallengesTitleModel)
class PublicCustomGroupChallengesTitleModelAdmin(admin.ModelAdmin):
    pass


# @admin.register(ParticipantsInBiddingGroupChallengesModel)
# class ParticipantsInBiddingGroupChallengesModelAdmin(admin.ModelAdmin):
#     pass

# @admin.register(ParticipantsInGroupChallengesForSubscribedUsersModel)
# class ParticipantsInGroupChallengesForSubscribedUsersModelAdmin(admin.ModelAdmin):
#     pass

# @admin.register(ParticipantsInGroupChallengesForFreeTrialModel)
# class ParticipantsInGroupChallengesForFreeTrialModelAdmin(admin.ModelAdmin):
#     pass

# @admin.register(ParticipantsInPublicCustomGroupChallengesModel)
# class ParticipantsInPublicCustomGroupChallengesModelAdmin(admin.ModelAdmin):
#     pass

# @admin.register(PublicCustomGroupChallengesPaymentModel)
# class PublicCustomGroupChallengesPaymentModelAdmin(admin.ModelAdmin):
#     pass

# @admin.register(RulesOfGroupChallengeModel)
# class RulesOfGroupChallengeModelAdmin(admin.ModelAdmin):
#     pass

# @admin.register(GuidelinesOfGroupChallengeModel)
# class GuidelinesOfGroupChallengeModelAdmin(admin.ModelAdmin):
#     pass

# @admin.register(WorkoutSuggestionsForGroupChallengeModel)
# class WorkoutSuggestionsForGroupChallengeModelAdmin(admin.ModelAdmin):
#     pass

# @admin.register(BiddingChallengePaymentDetailsModel)
# class BiddingChallengePaymentDetailsModelAdmin(admin.ModelAdmin):
#     pass

# @admin.register(PrivateCustomGroupChallengesModel)
# class PrivateCustomGroupChallengesModelAdmin(admin.ModelAdmin):
#     pass

# @admin.register(ParticipantsInPrivateCustomGroupChallengesModel)
# class ParticipantsInPrivateCustomGroupChallengesModelAdmin(admin.ModelAdmin):
#     pass

# @admin.register(PrivateCustomGroupChallengesPaymentModel)
# class PrivateCustomGroupChallengesPaymentModelAdmin(admin.ModelAdmin):
#     pass
