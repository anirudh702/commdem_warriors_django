from django.contrib import admin

from bidding_contest.models import (
    AnswersOfBiddingContestModel,
    BiddingContestModel,
    BiddingContestPaymentModel,
    ParticipantsInBiddingContestModel,
    QuestionsForBiddingContestModel,
)


# Register your models here.
@admin.register(BiddingContestModel)
class BiddingContestModelAdmin(admin.ModelAdmin):
    pass


@admin.register(ParticipantsInBiddingContestModel)
class ParticipantsInBiddingContestModelAdmin(admin.ModelAdmin):
    pass


@admin.register(BiddingContestPaymentModel)
class BiddingContestPaymentModelAdmin(admin.ModelAdmin):
    pass


@admin.register(QuestionsForBiddingContestModel)
class QuestionsForBiddingContestModelAdmin(admin.ModelAdmin):
    pass


@admin.register(AnswersOfBiddingContestModel)
class AnswersOfBiddingContestModelAdmin(admin.ModelAdmin):
    pass
