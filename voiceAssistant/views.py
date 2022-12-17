from rest_framework.decorators import api_view
from firebase.firebase import send_to_firebase
from location.models import CitiesModel, CountriesDialCodeModel,StatesModel,CountriesModel
from rest_framework.response import Response
from response import Response as ResponseData
from rest_framework import status
from user.models import UserModel

from voiceAssistant.models import userPreferredVoiceLanguageModel, voiceAssistantLanguagesModel
# Create your views here.

@api_view(["POST"])
def addNewLanguage(request):
    """Function to add new language for our voice assistant"""
    try:
        data = request.data
        print(type(data))
        for key,value in dict(data).items():
            print(f"{key} {value}")
            data_exist_or_not = voiceAssistantLanguagesModel.objects.filter(language_code=key,language_name=value).first()
            if data_exist_or_not is None:
               new_language = voiceAssistantLanguagesModel.objects.create(
                language_code=key,
                language_name=value,
            )
               new_language.save()
        return Response(
            ResponseData.success(
                [], "Data added successfully"),
            status=status.HTTP_201_CREATED,
        )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["POST"])
def get_all_languages(request):
    """Function to get all languages details"""
    try:
        # send_to_firebase()
        languages_data = voiceAssistantLanguagesModel.objects.values().filter().all()
        for i in range(0,len(languages_data)):
            languages_data[i].pop('created_at')
            languages_data[i].pop('updated_at')
            languages_data[i].pop('language_code')
        return Response(
            ResponseData.success(
                languages_data, "Languages details fetched successfully"),
            status=status.HTTP_201_CREATED)
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["POST"])
def addUserPrefferedLanguage(request):
    """Function to add voice assistant language for a user"""
    try:
        data = request.data
        data_exist_or_not = voiceAssistantLanguagesModel.objects.filter(id=data['voice_id']).first()
        if data_exist_or_not is None:
            return Response(
                ResponseData.success_without_data("Voice id is invalid"),
                status=status.HTTP_201_CREATED,
            )
        user_data_exist_or_not = userPreferredVoiceLanguageModel.objects.filter(voice_assistant_language_id=data['voice_id'],user_id=data['user_id']).first()
        if user_data_exist_or_not is not None:
            return Response(
                ResponseData.success_without_data("User language already exists in our database"),
                status=status.HTTP_201_CREATED,
            )
        user_language_data = userPreferredVoiceLanguageModel.objects.create(
            user=UserModel(id=data['user_id']),
            voice_assistant_language=voiceAssistantLanguagesModel(id=data['voice_id']),
        )
        user_language_data.save()
        return Response(
                ResponseData.success(
                    [], "User language added successfully"),
                status=status.HTTP_201_CREATED,
            )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["POST"])
def get_user_preferred_language(request):
    """Function to get user preferred language details"""
    try:
        user_language_data = userPreferredVoiceLanguageModel.objects.values().filter(user_id=request.data['user_id']).all()
        for i in range(0,len(user_language_data)):
            user_language_data[i].pop('created_at')
            user_language_data[i].pop('updated_at')
        return Response(
            ResponseData.success(
                user_language_data, "User Language details fetched successfully"),
            status=status.HTTP_201_CREATED)
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
