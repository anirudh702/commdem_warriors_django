from django.contrib import admin

from voiceAssistant.models import (
    voiceAssistantAfterUpdateMessageModel,
    voiceAssistantBeforeUpdateMessageModel,
)


# Register your models here.
@admin.register(voiceAssistantBeforeUpdateMessageModel)
class VoiceAssistantBeforeUpdateMessageModelAdmin(admin.ModelAdmin):
    list_filter = (("occupation", admin.RelatedOnlyFieldListFilter),)
    search_fields = ["id"]
    pass


@admin.register(voiceAssistantAfterUpdateMessageModel)
class VoiceAssistantAfterUpdateMessageModelAdmin(admin.ModelAdmin):
    list_filter = (("commitment_category", admin.RelatedOnlyFieldListFilter),)
    pass
