from django.contrib import admin

from logs.models import (
    LogsOfPagesOfUserModel,
    LogsOfUserProgressTapModel,
    LogsOfUserTapOnAdvertisementModel,
)


# Register your models here.
@admin.register(LogsOfPagesOfUserModel)
class LogsOfPagesOfUserModelAdmin(admin.ModelAdmin):
    list_filter = (("user__full_name"), ("created_at"))
    pass


# Register your models here.
@admin.register(LogsOfUserProgressTapModel)
class LogsOfUserProgressTapModelAdmin(admin.ModelAdmin):
    list_filter = (("from_user__full_name"), ("to_user__full_name"), ("created_at"))
    pass


# Register your models here.
@admin.register(LogsOfUserTapOnAdvertisementModel)
class LogsOfUserTapOnAdvertisementModelAdmin(admin.ModelAdmin):
    list_filter = (("user__full_name"), ("created_at"))
    pass
