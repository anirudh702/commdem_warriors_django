from datetime import datetime
import datetime as dt
from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework.decorators import api_view
from group_challenges.models import GroupChallengesModel, GuidelinesOfGroupChallengeModel, ParticipantsInGroupChallengeModel, RulesOfGroupChallengeModel
from group_challenges.serializers import AddNewUserInGroupChallengeSerializer, GetAllParticipantsOfGroupChallengeSerializer, GetGroupChallengesSerializer, UpdateUserParticipationStatusInGroupChallengeSerializer, UploadVideoOfUserGroupChallengeSerializer
from rest_framework.response import Response
from response import Response as ResponseData
from rest_framework import status
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from soloCompetitionsForFreeTrialUsers.models import FreeTrialSoloChallengesModel, ParticipantsInSoloChallengeModel, RulesOfSoloChallengesModel, WorkoutSuggestionsForSoloChallengeModel
from soloCompetitionsForFreeTrialUsers.serializers import UploadVideoOfUserSoloChallengeSerializer
from user.models import UserHealthDetailsModel, UserModel, UserPaymentDetailsModel
from commitment.models import CommitmentCategoryModel, CommitmentModel

# Create your views here.
@api_view(["POST"])
def get_all_solo_challenges(request):
    """Function to get solo challenges based on date"""
    try:
        data = request.data
        print(f"data {data}")
        user = UserModel.objects.filter(id=request.data['user_id'],is_active=True).first()
        if not user:
                   return Response(
                       ResponseData.error("User id is invalid"),
                       status=status.HTTP_200_OK,
                   )
        serializer = GetGroupChallengesSerializer(data=data)
        if serializer.is_valid():
            print("true")
            user_id = serializer.data['user_id']
            challenges_data = FreeTrialSoloChallengesModel.objects.values().all()
            if len(challenges_data) == 0:
                    return Response(
                       ResponseData.success(
                           [], "No solo challenge found"),
                       status=status.HTTP_201_CREATED)
            for i in range(0,len(challenges_data)):
                challenges_data[i]['suggested_workout'] = FreeTrialSoloChallengesModel(**challenges_data[i]).suggested_workout.values('mainTitle','id').all()
                last_payment = UserPaymentDetailsModel.objects.values().filter(user_id=user_id,is_active=True).last()['date_of_payment'].date()
                challenges_data[i]['challenge_rules'] = RulesOfSoloChallengesModel.objects.values().filter().all()
                for j in range(0,len(challenges_data[i]['challenge_rules'])):
                    challenges_data[i]['challenge_rules'][j].pop('created_at')
                    challenges_data[i]['challenge_rules'][j].pop('updated_at')
                challenges_data[i]['has_user_submitted_video'] = False
                challenges_data[i]['challenge_video'] = ''
                challenges_data[i]['is_user_participating'] = True
                if i == 0:
                    challenges_data[i]['date_of_challenge'] = last_payment + dt.timedelta(days=7)
                else:
                    challenges_data[i]['date_of_challenge'] = last_payment + dt.timedelta(days=13)
                is_user_participant = ParticipantsInSoloChallengeModel.objects.filter(user_id=user_id,solo_challenge_id=challenges_data[i]['id']).first()
                if is_user_participant is not None:
                    challenges_data[i]['has_user_submitted_video'] = is_user_participant.has_submitted_video
                    challenges_data[i]['challenge_video'] = f"{is_user_participant.challenge_video}"           
            for i in range(0,len(challenges_data)):
                challenges_data[i].pop('created_at')
                challenges_data[i].pop('updated_at')
            return Response(
                       ResponseData.success(
                           challenges_data, "Solo Challenges fetched successfully"),
                       status=status.HTTP_201_CREATED)
        return Response(
                    ResponseData.error(serializer.errors),
                    status=status.HTTP_400_BAD_REQUEST,
                )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["POST"])
def upload_video_for_solo_challenge(request):
    """Function to upload solo challenge video of a user"""
    try:
        data = request.data
        print(f"data {data}")
        serializer = UploadVideoOfUserSoloChallengeSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            solo_challenge_id = serializer.data["solo_challenge_id"]
            video_file = request.FILES['video_file']
            is_updated_file = request.data["is_updated_file"]
            user = UserModel.objects.filter(id=user_id,is_active=True).first()
            if not user:
                   return Response(
                       ResponseData.error("User id is invalid"),
                       status=status.HTTP_200_OK,
                   )
            solo_challenge = FreeTrialSoloChallengesModel.objects.filter(id=solo_challenge_id).first()
            if not solo_challenge:
                   return Response(
                       ResponseData.error("Solo challenge id is invalid"),
                       status=status.HTTP_200_OK,
                   )
            user_challenge_data = ParticipantsInSoloChallengeModel.objects.filter(user_id=user_id,solo_challenge_id=solo_challenge_id,hide_from_user=False).get()
            if is_updated_file == True:
                print(f"user_challenge_data.challenge_video {user_challenge_data.challenge_video}")
                fs = FileSystemStorage(location='static/')
                fs.delete(str(user_challenge_data.challenge_video).split("/")[1])
            user_challenge_data.challenge_video = f"static/{video_file}"
            user_challenge_data.has_submitted_video = True
            user_challenge_data.save()
            if video_file!="" or video_file is not None:
                 fs = FileSystemStorage(location='static/')
                 fs.save(video_file.name, video_file)
            return Response(
                ResponseData.success_without_data(
                    "Video uploaded successfully"),
                status=status.HTTP_201_CREATED,
            )   
        for error in serializer.errors:
            print(serializer.errors[error][0])
        return Response(
            ResponseData.error(serializer.errors[error][0]),
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
