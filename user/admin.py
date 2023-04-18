from django.contrib import admin
from user.models import UserModel, UserPaymentDetailsModel, UserPrivacyModel, UserSubscriptionDetailsModel, UserWisePrivacyModel,UserHealthDetailsModel
from voiceAssistant.models import userPreferredVoiceLanguageModel

# Register your models here.
@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    pass

@admin.register(UserPaymentDetailsModel)
class UserPaymentDetailsModelAdmin(admin.ModelAdmin):
    pass

@admin.register(UserHealthDetailsModel)
class UserHealthDetailsModelAdmin(admin.ModelAdmin):
    pass

@admin.register(UserSubscriptionDetailsModel)
class UserSubscriptionDetailsModelAdmin(admin.ModelAdmin):
    pass

@admin.register(userPreferredVoiceLanguageModel)
class UserPreferredVoiceLanguageModelAdmin(admin.ModelAdmin):
    pass   

@admin.register(UserPrivacyModel)
class UserPrivacyModelAdmin(admin.ModelAdmin):
    pass   

@admin.register(UserWisePrivacyModel)
class UserWisePrivacyModelAdmin(admin.ModelAdmin):
    pass   