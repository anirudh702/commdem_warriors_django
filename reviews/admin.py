from django.contrib import admin

from reviews.models import ReviewModel


# Register your models here.
@admin.register(ReviewModel)
class ReviewModelAdmin(admin.ModelAdmin):
    pass
