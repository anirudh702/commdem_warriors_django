
"""
Api end points for review module
"""

from django.urls import path
from reviews import views


urlpatterns = [
    path('add_review/', views.add_review, name="add_review"),
    path('get_all_review/', views.get_all_review, name="get_all_review"),
    path('get_review_by_id/', views.get_review_by_id, name="get_review_by_id"),
    path('delete_all_review/', views.delete_all_review, name="delete_review"),
    path('delete_review_by_id/', views.delete_review_by_id, name="delete_review_by_id"),
    path('update_review/', views.update_review, name="update_review"),
]


                  