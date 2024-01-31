from django.contrib import admin

from app_info_videos.models import AppInfoVideosModel


# Register your models here.
@admin.register(AppInfoVideosModel)
class AppInfoVideosModelAdmin(admin.ModelAdmin):
    pass
