from django.contrib import admin
from user.models import UserModel, UserPaymentDetailsModel, UserSubscriptionDetailsModel
from voiceAssistant.models import userPreferredVoiceLanguageModel

# Register your models here.
@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    pass

@admin.register(UserPaymentDetailsModel)
class UserPaymentDetailsModelAdmin(admin.ModelAdmin):
    pass

@admin.register(UserSubscriptionDetailsModel)
class UserSubscriptionDetailsModelAdmin(admin.ModelAdmin):
    pass

@admin.register(userPreferredVoiceLanguageModel)
class UserPreferredVoiceLanguageModelAdmin(admin.ModelAdmin):
    pass    