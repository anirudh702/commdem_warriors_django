"""
Api end points for user_auth module
"""

from django.urls import path
from voiceAssistant import views


urlpatterns = [
    # path('addCountryDialCodes/', views.addCountryDialCodes, name="addCountryDialCodes"),
    path('addNewLanguage/', views.addNewLanguage, name="addNewLanguage"),  
    path('addVoiceAssistantMessageAfterUpdate/', views.addVoiceAssistantMessageAfterUpdate, name="addVoiceAssistantMessageAfterUpdate"), 
    path('addAllAfterUpdateVoicesLocally/', views.addAllAfterUpdateVoicesLocally, name="addAllAfterUpdateVoicesLocally"), 
    path('addVoiceAssistantMessageBeforeUpdate/', views.addVoiceAssistantMessageBeforeUpdate, name="addVoiceAssistantMessageBeforeUpdate"),  
    path('get_all_languages/', views.get_all_languages, name="get_all_languages"),  
    path('get_voice_assistant_message_before_update/', views.get_voice_assistant_message_before_update, name="get_voice_assistant_message_before_update"),  
    path('addUserPrefferedLanguage/', views.addUserPrefferedLanguage, name="addUserPrefferedLanguage"),
    path('get_user_preferred_language/', views.get_user_preferred_language, name="get_user_preferred_language"),
    path('addUserCommitmentVoiceBeforeUpdate/', views.addUserCommitmentVoiceBeforeUpdate, name="addUserCommitmentVoiceBeforeUpdate"),
    path('addUserVoiceForNextDayCommitment/', views.addUserVoiceForNextDayCommitment, name="addUserVoiceForNextDayCommitment"),
]
