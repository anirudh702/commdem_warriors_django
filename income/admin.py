from django.contrib import admin

from oneToOneChatModule.models import OneToOneChatModel

# Register your models here.
@admin.register(OneToOneChatModel)
class OneToOneChatModelAdmin(admin.ModelAdmin):
    pass