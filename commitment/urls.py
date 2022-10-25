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
    path('get_commitment/', views.get_commitments, name="get_commitments"),
]
