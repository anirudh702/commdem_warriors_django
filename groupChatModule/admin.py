from django.contrib import admin

from groupChatModule.models import GroupChatModel


# Register your models here.
@admin.register(GroupChatModel)
class GroupChatModelAdmin(admin.ModelAdmin):
    pass
