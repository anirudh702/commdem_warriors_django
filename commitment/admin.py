from django.contrib import admin
from commitment.models import CauseOfCategorySuccessOrFailureModel, CommitmentCategoryModel, CommitmentGraphDataModel, CommitmentModel, CommitmentNameModel, ReasonBehindCommitmentSuccessOrFailureForUser

# Register your models here.
@admin.register(CommitmentCategoryModel)
class CommitmentCategoryModelAdmin(admin.ModelAdmin):
    pass

# Register your models here.
@admin.register(CommitmentNameModel)
class CommitmentNameModelAdmin(admin.ModelAdmin):
    pass

# Register your models here.
@admin.register(CauseOfCategorySuccessOrFailureModel)
class CauseOfCategorySuccessOrFailureModelAdmin(admin.ModelAdmin):
    pass

# Register your models here.
@admin.register(CommitmentModel)
class CommitmentModelAdmin(admin.ModelAdmin):
    pass

# Register your models here.
@admin.register(ReasonBehindCommitmentSuccessOrFailureForUser)
class ReasonBehindCommitmentSuccessOrFailureForUserAdmin(admin.ModelAdmin):
    pass

# Register your models here.
@admin.register(CommitmentGraphDataModel)
class CommitmentGraphDataModelAdmin(admin.ModelAdmin):
    pass