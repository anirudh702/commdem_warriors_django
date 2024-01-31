from django.contrib import admin

from questions_before_relationship.models import (
    QuestionsToAskBeforeModel,
    mcqsChoicesModel,
)


# Register your models here.
@admin.register(QuestionsToAskBeforeModel)
class QuestionsToAskBeforeModelAdmin(admin.ModelAdmin):
    pass


@admin.register(mcqsChoicesModel)
class mcqsChoicesModelAdmin(admin.ModelAdmin):
    pass
