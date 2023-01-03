"""
Api end points for user_auth module
"""

from django.urls import path
from commitment import views


urlpatterns = [
    path('add_commitment/', views.add_new_commitment, name="add_commitment"),
    path('add_commitment_category/', views.add_new_commitment_category, name="add_commitment_category"),
    path('add_commitment_name/', views.add_new_commitment_name, name="add_commitment_name"),
    path('get_commitment_category_with_name/', views.get_commitment_category_with_name, name="get_commitment_category_with_name"),
    path('get_commitment_name/', views.get_commitment_name, name="get_commitment_name"),
    path('get_user_commitment/', views.get_user_commitments, name="get_user_commitments"),
    path('get_all_commitment/', views.get_all_commitments, name="get_all_commitments"),
    path('get_other_users_commitments/', views.get_other_users_commitments, name="get_other_users_commitments"),
    path('get_user_commitments_by_commitment_date/', views.get_user_commitments_by_commitment_date_only, name="get_user_commitments_by_commitment_date_only"),
    path('share_user_commitment_on_whatsapp/', views.share_user_commitment_on_whatsapp, name="share_user_commitment_on_whatsapp"),
    path('get_group_commitments_by_commitment_date/', views.get_group_commitments_by_commitment_date_only, name="get_group_commitments_by_commitment_date_only"),
    path('get_user_commitments_by_start_end_date/', views.get_user_commitments_by_start_end_date_only, name="get_user_commitments_by_start_end_date_only"),
    path('get_group_commitments_by_start_end_date/', views.get_group_commitments_by_start_end_date_only, name="get_group_commitments_by_start_end_date_only"),
    path('update_commitment/', views.update_commitment, name="update_commitment"),
    path('update_exercise_model/', views.update_exercise_model, name="update_exercise_model"),
    path('add_cause_of_category_success_or_failure/', views.add_cause_of_category_success_or_failure, name="add_cause_of_category_success_or_failure"),
    path('get_cause_of_category_success_or_failure/', views.get_cause_of_category_success_or_failure, name="get_cause_of_category_success_or_failure"),
]
