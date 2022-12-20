import django
import gtts
from rest_framework.decorators import api_view
from commitment.models import CommitmentModel, CommitmentNameModel, next_day_datetime
from firebase.firebase import send_to_firebase
from location.models import CitiesModel, CountriesDialCodeModel,StatesModel,CountriesModel
from rest_framework.response import Response
from response import Response as ResponseData
from rest_framework import status
from user.models import UserHealthDetailsModel, UserModel, UserProfessionalDetailsModel
from datetime import datetime, timedelta
from django.utils.timezone import localtime, now
from voiceAssistant.models import userCommitmentVoiceBeforeUpdateModel, userPreferredVoiceLanguageModel, voiceAssistantLanguagesModel
from voiceAssistant.serializers import AddUserCommitmentVoiceFileSerializer
from googletrans import Translator
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
                languageCode=key,
                languageName=value,
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
            languages_data[i].pop('languageCode')
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

@api_view(["POST"])
def addUserCommitmentVoiceBeforeUpdate(request):
    """Function to add user commitment voice file before he/she updates the commitment"""
    try:
        data = request.data
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
def addUserCommitmentVoiceBeforeUpdate(request):
    """Function to add user commitment voice file before he/she updates the commitment"""
    try:
        data = request.data
        print(data)
        serializer = AddUserCommitmentVoiceFileSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            user = UserModel.objects.filter(
                id=user_id,is_active=True).first()
            if not user:
                return Response(
                    ResponseData.error(
                        "User id is invalid"),
                    status=status.HTTP_201_CREATED,
                )
            next_date = str(datetime.now().date() + timedelta(days=1))
            today_date = str(datetime.now().date() + timedelta(days=0))
            next_day = str(datetime.now().day)
            add_this_to_voice = ""
            if(next_day == 'Saturday' or next_day == 'Sunday'):
                add_this_to_voice = f'I know today is {next_day}, you would be in your chilling mood.'
            print(f"next_day {next_date}")
            commitment_details = CommitmentModel.objects.values().filter(user_id=user_id,commitment_date__icontains=next_day).all()
            if len(commitment_details) == 0: 
             return Response(
                ResponseData.success_without_data(
                    "No commitment found for tomorrow's date"),
                status=status.HTTP_201_CREATED)
            user_profession_details = UserProfessionalDetailsModel.objects.filter(
                user_id=user_id).first().designation__title
            user_designation = ''
            if(str(user_profession_details).__contains__('Job')):
                user_designation = 'doing job'
            if(str(user_profession_details).__contains__('Business')):
                user_designation = 'doing business'
            if(str(user_profession_details).__contains__('Student')):
                user_designation = 'a student'
            if(str(user_profession_details).__contains__('Freelancer')):
                user_designation = 'a freelancer'
            user_gender_details = UserHealthDetailsModel.objects.filter(
                user_id=user_id).first().gender
            user_gender = ''
            if(str(user_gender_details).__contains__('Male')):
                user_gender = 'Brother, '
            elif(str(user_gender_details).__contains__('Female')):
                user_gender = "Ma'am, "
            elif(str(user_gender_details).__contains__('Transgender')):
                user_gender = 'Sir, '
            user_selected_language = userPreferredVoiceLanguageModel.objects.filter(
                user_id=user_id).first().voice_assistant_language.languageCode
            joining_date_of_user = user.joining_date
            date_format = "%Y-%m-%d"
            a = datetime.strptime(str(joining_date_of_user.date()), date_format)
            b = datetime.strptime(next_date, date_format)
            delta = b - a
            days_passed_after_joining = delta.days
            translator = Translator()
            if(days_passed_after_joining == 1):
                final_data = []
                for i in range(0,len(commitment_details)):
                    is_data_exists = userCommitmentVoiceBeforeUpdateModel.objects.filter(
                            user_id=user_id,commitment__commitment_date__icontains=next_date,commitment=CommitmentModel(id=commitment_details[i]['id'])).first()
                    if is_data_exists:
                            return Response(
                                ResponseData.error(
                                    "Voice message for this day commitment already exists in our database"),
                                status=status.HTTP_201_CREATED,
                            )
                    category_name = commitment_details[i]['category_data']['name']
                    if(str(category_name).__contains__('Exercise')):
                        local_audio_path = f"{user_id}_{datetime.now()}"
                        translated_text = translator.translate(f'Hi {str(user.full_name).split(" ")[0]},I know you are {user_designation}. As it is your first day with our family, I request you to start it slowly, but remember that other commitments depend on how you do this commitment',dest=user_selected_language)
                        tts = gtts.gTTS(translated_text.text,
                        lang = user_selected_language,slow=False,tld='co.in')
                        final_data.append(userCommitmentVoiceBeforeUpdateModel(
                                    user=UserModel(id=user_id),
                            commitment=CommitmentModel(id=commitment_details[i]['id']),    
                            audio_file_path=f"static/{local_audio_path}.mp3",
                                    ))
                        tts.save(f"static/{local_audio_path}.mp3")
                    elif(str(category_name).__contains__('Food')):
                        local_audio_path = f"{user_id}_{datetime.now()}"
                        translated_text = translator.translate(f'I am sure you want a great start, If you feel like having junk food today, please re-think why you joined our commdem warriors group',dest=user_selected_language)
                        tts = gtts.gTTS(translated_text.text,
                        lang = user_selected_language,slow=False,tld='co.in')
                        final_data.append(userCommitmentVoiceBeforeUpdateModel(
                                    user=UserModel(id=user_id),
                            commitment=CommitmentModel(id=commitment_details[i]['id']),    
                            audio_file_path=f"static/{local_audio_path}.mp3",
                                    ))
                        tts.save(f"static/{local_audio_path}.mp3")
                    elif(str(category_name).__contains__('Water')):
                        local_audio_path = f"{user_id}_{datetime.now()}"
                        translated_text = translator.translate(f'To fullfil your water commitment, just think what are some ways by which {str(user.full_name).split(" ")[0]} cannot forget to drink water, I am sure you will find an answer yourself',dest=user_selected_language)
                        tts = gtts.gTTS(translated_text.text,
                        lang = user_selected_language,slow=False,tld='co.in')
                        final_data.append(userCommitmentVoiceBeforeUpdateModel(
                                    user=UserModel(id=user_id),
                            commitment=CommitmentModel(id=commitment_details[i]['id']),    
                            audio_file_path=f"static/{local_audio_path}.mp3",
                                    ))
                        tts.save(f"static/{local_audio_path}.mp3")
                userCommitmentVoiceBeforeUpdateModel.objects.bulk_create(final_data)
            elif(days_passed_after_joining == 2):
                final_data = []
                for i in range(0,len(commitment_details)):
                    is_data_exists = userCommitmentVoiceBeforeUpdateModel.objects.filter(
                            user_id=user_id,commitment__commitment_date__icontains=next_date,commitment=CommitmentModel(id=commitment_details[i]['id'])).first()
                    if is_data_exists:
                            return Response(
                                ResponseData.error(
                                    "Voice message for this day commitment already exists in our database"),
                                status=status.HTTP_201_CREATED,
                            )
                    category_name = commitment_details[i]['category_data']['name']
                    if(str(category_name).__contains__('Exercise')):
                        text = f"Hi {str(user.full_name).split(' ')[0]},"
                        was_yesterday_commitment_done = CommitmentModel.objects.filter(id=commitment_details[i]['id'],commitment_date__icontains=today_date).first()
                        if was_yesterday_commitment_done is None:
                            text += 'It is fine if you did not give exercise commitment yesterday, today I want you to give your 100% to it. I know you can do it.'
                        elif was_yesterday_commitment_done is not None:
                            if was_yesterday_commitment_done.is_updated == False:
                                text += 'As it is just a starting, I request you not to forget updating. It is ok if you could not do it, but we need an update from your end to support you'
                            elif was_yesterday_commitment_done.is_done == False:
                                text+='It is just a beginning my dear friend. It is ok if you could not achieve it yesterday, today I just want you to think how you can spare 30 min out of 24 hours for your health, I am 100% sure you will do it today.'
                            elif was_yesterday_commitment_done.is_done == True:
                                text+='First of all, your family is really happy that you did exercise yesterday, I just want you to realize how did exercise change your day, I am sure today also you will achieve this commitment'
                        local_audio_path = f"{user_id}_{datetime.now()}"
                        translated_text = translator.translate(text,dest=user_selected_language)
                        tts = gtts.gTTS(translated_text.text,
                        lang = user_selected_language,slow=False,tld='co.in')
                        final_data.append(userCommitmentVoiceBeforeUpdateModel(
                                    user=UserModel(id=user_id),
                            commitment=CommitmentModel(id=commitment_details[i]['id']),    
                            audio_file_path=f"static/{local_audio_path}.mp3",
                                    ))
                        tts.save(f"static/{local_audio_path}.mp3")
                    elif(str(category_name).__contains__('Food')):
                        text = f'Hello {str(user.full_name).split(" ")[0]}, {add_this_to_voice}. '
                        was_yesterday_commitment_done = CommitmentModel.objects.filter(id=commitment_details[i]['id'],commitment_date__icontains=today_date).first()
                        if was_yesterday_commitment_done is None:
                            text += 'We know you could not give food commitment yesterday.Please ask yourself why you did not do that. But I am glad today you gave food commitment'
                        elif was_yesterday_commitment_done is not None:
                            if was_yesterday_commitment_done.is_updated == False:
                                text += 'I hope you trust our process. I am requesting you please update your commitment. At the last, we are all here to support each other'
                            elif was_yesterday_commitment_done.is_done == False:
                                text+= 'My friend, if you are facing any issue on how to self control yourself, please talk with leaders in the group. Today I want you to challenge yourself for finishing this commitment'
                            elif was_yesterday_commitment_done.is_done == True:
                                text+='Cheers,yesterday you finished this commitment. I am sure that happiness was amazing. Let us repeat that today.'
                        local_audio_path = f"{user_id}_{datetime.now()}"
                        translated_text = translator.translate(text,dest=user_selected_language)
                        tts = gtts.gTTS(translated_text.text,
                        lang = user_selected_language,slow=False,tld='co.in')
                        final_data.append(userCommitmentVoiceBeforeUpdateModel(
                                    user=UserModel(id=user_id),
                            commitment=CommitmentModel(id=commitment_details[i]['id']),    
                            audio_file_path=f"static/{local_audio_path}.mp3",
                                    ))
                        tts.save(f"static/{local_audio_path}.mp3")
                    elif(str(category_name).__contains__('Water')):
                        text = ''
                        was_yesterday_commitment_done = CommitmentModel.objects.filter(id=commitment_details[i]['id'],commitment_date__icontains=today_date).first()
                        if was_yesterday_commitment_done is None:
                            text += 'Yesterday I was very sad because you did not give water commitment. Remember, water is equally important as food and exercise'
                        elif was_yesterday_commitment_done is not None:
                            if was_yesterday_commitment_done.is_updated == False:
                                text += f'{user_gender}, yesterday we did not get an update of this commitment. Please set reminder to update this commitment today'
                            elif was_yesterday_commitment_done.is_done == False:
                                text+= 'Please ask yourself,the reason you gave yesterday was there a solution for that. I want you to think how can you find an alternative to fulfill this commitment today.'
                            elif was_yesterday_commitment_done.is_done == True:
                                text+='I slept very peacefully yesterday because you finished this commitment, I am very grateful for you. Thank you so much'
                        local_audio_path = f"{user_id}_{datetime.now()}"
                        translated_text = translator.translate(text,dest=user_selected_language)
                        tts = gtts.gTTS(translated_text.text,
                        lang = user_selected_language,slow=False,tld='co.in')
                        final_data.append(userCommitmentVoiceBeforeUpdateModel(
                                    user=UserModel(id=user_id),
                            commitment=CommitmentModel(id=commitment_details[i]['id']),    
                            audio_file_path=f"static/{local_audio_path}.mp3",
                                    ))
                        tts.save(f"static/{local_audio_path}.mp3")
                userCommitmentVoiceBeforeUpdateModel.objects.bulk_create(final_data)
            user_voice_data = userCommitmentVoiceBeforeUpdateModel.objects.values().filter(
                user=UserModel(id=user_id),
                commitment=CommitmentModel(id=commitment_details[i]['id'])).all()
            for i in range(0,len(user_voice_data)):
                user_voice_data[i].pop('created_at')
                user_voice_data[i].pop('updated_at')
            return Response(
                ResponseData.success(
                    user_voice_data, "Data added successfully"),
                status=status.HTTP_201_CREATED,
            )
        return Response( 
                    ResponseData.error(serializer.errors),
                    status=status.HTTP_400_BAD_REQUEST,
                )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )