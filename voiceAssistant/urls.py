"""
Api end points for user_auth module
"""

from django.urls import path
from voiceAssistant import views


urlpatterns = [
    # path('addCountryDialCodes/', views.addCountryDialCodes, name="addCountryDialCodes"),
    path('addNewLanguage/', views.addNewLanguage, name="addNewLanguage"),  
    path('get_all_languages/', views.get_all_languages, name="get_all_languages"),  
    path('addUserPrefferedLanguage/', views.addUserPrefferedLanguage, name="addUserPrefferedLanguage"),
    path('get_user_preferred_language/', views.get_user_preferred_language, name="get_user_preferred_language"),
]
