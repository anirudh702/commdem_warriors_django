from datetime import datetime
from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework.decorators import api_view
from group_challenges.models import GroupChallengesModel, ParticipantsInGroupChallengeModel
from group_challenges.serializers import AddNewUserInGroupChallengeSerializer, GetAllParticipantsOfGroupChallengeSerializer, GetGroupChallengesSerializer, UpdateUserParticipationStatusInGroupChallengeSerializer, UploadVideoOfUserGroupChallengeSerializer
from rest_framework.response import Response
from response import Response as ResponseData
from rest_framework import status
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from user.models import UserHealthDetailsModel, UserModel

# Create your views here.
@api_view(["POST"])
def get_all_group_challenges(request):
    """Function to get group challenges based on date"""
    try:
        data = request.data
        user = UserModel.objects.filter(id=request.data['user_id'],is_active=True).first()
        if not user:
                   return Response(
                       ResponseData.error("User id is invalid"),
                       status=status.HTTP_200_OK,
                   )
        serializer = GetGroupChallengesSerializer(data=data)
        if serializer.is_valid():
            date = serializer.data['date']
            user_id = serializer.data['user_id']
            page_number = int(serializer.data['page_no'] if 'page_no' in request.data else 0)
            page_size_param = int(serializer.data['page_size'] if 'page_size' in request.data else 0)
            page_no = page_number
            page_size = page_size_param
            start=(page_no-1)*page_size
            end=page_no*page_size
            today_date = datetime.now().date()
            if date is not None:
                challenges_data = GroupChallengesModel.objects.values().filter(start_date__lte=date,end_date__gte=date).order_by('-created_at').all()[start:end]
            else:
                challenges_data = GroupChallengesModel.objects.values().order_by('-created_at').all()[start:end]
            if len(challenges_data) == 0:
                    return Response(
                       ResponseData.success(
                           [], "No group challenge found"),
                       status=status.HTTP_201_CREATED)
            for i in range(0,len(challenges_data)):
                user_age = UserHealthDetailsModel.objects.filter(user_id=user_id).first().age
                challenges_data[i]['is_user_between_this_age'] = False
                challenges_data[i]['is_participation_allowed'] = False
                challenges_data[i]['is_past_competition'] = False
                challenges_data[i]['is_future_competition'] = False
                if(user_age>=challenges_data[i]['min_age'] and user_age<=challenges_data[i]['max_age']):
                    challenges_data[i]['is_user_between_this_age'] = True
                if(challenges_data[i]['start_date'] <= today_date and challenges_data[i]['end_date'] >= today_date):
                    challenges_data[i]['is_participation_allowed'] = True
                if(challenges_data[i]['end_date'] < today_date ):
                    challenges_data[i]['is_past_competition'] = True
                if(challenges_data[i]['start_date'] > today_date ):
                    challenges_data[i]['is_future_competition'] = True
                challenges_data[i].pop('created_at')
                challenges_data[i].pop('updated_at')
                challenges_data[i]['total_participants'] = len(ParticipantsInGroupChallengeModel.objects.filter(group_challenge_id=challenges_data[i]['id']).all())
                challenges_data[i]['total_videos_submitted'] = len(ParticipantsInGroupChallengeModel.objects.filter(group_challenge_id=challenges_data[i]['id'],has_submitted_video=True).all())
            return Response(
                       ResponseData.success(
                           challenges_data, "Challenges fetched successfully"),
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
def get_all_participants_of_group_challenge(request):
    """Function to get all users participated in group challenge"""
    try:
        data = request.data
        group_challenge = GroupChallengesModel.objects.filter(id=request.data['group_challenge_id']).first()
        if not group_challenge:
                   return Response(
                       ResponseData.error("Group challenge id is invalid"),
                       status=status.HTTP_200_OK,
                   )
        serializer = GetAllParticipantsOfGroupChallengeSerializer(data=data)
        if serializer.is_valid():
            group_challenge_id = serializer.data['group_challenge_id']
            page_number = int(serializer.data['page_no'] if 'page_no' in request.data else 0)
            page_size_param = int(serializer.data['page_size'] if 'page_size' in request.data else 0)
            page_no = page_number
            page_size = page_size_param
            start = (page_no-1)*page_size
            end = page_no*page_size
            challenge_data = ParticipantsInGroupChallengeModel.objects.values().filter(group_challenge_id=group_challenge_id,hide_from_user=False).all()[start:end]
            if len(challenge_data) == 0:
                    return Response(
                       ResponseData.success(
                           [], "No participant found"),
                       status=status.HTTP_201_CREATED)
            for i in range(0,len(challenge_data)):
                challenge_data[i]['user_data'] = UserModel.objects.values().filter(id=challenge_data[i]['user_id']).first()
                challenge_data[i].pop('user_id')
                challenge_data[i]['user_data'].pop('updated_at')
                challenge_data[i]['user_data'].pop('created_at')
                challenge_data[i].pop('updated_at')
                challenge_data[i].pop('created_at')
                challenge_data[i].pop('hide_from_user')
                if(challenge_data[i]['date_of_submission'] is None):
                    challenge_data[i]['date_of_submission'] = ""
            return Response(
                       ResponseData.success(
                           challenge_data, "User details fetched successfully"),
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
def add_user_in_group_challenge(request):
    """Function to add user in a group challenge"""
    try:
        data = request.data
        serializer = AddNewUserInGroupChallengeSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            group_challenge_id = serializer.data["group_challenge_id"]
            user = UserModel.objects.filter(id=user_id,is_active=True).first()
            if not user:
                   return Response(
                       ResponseData.error("User id is invalid"),
                       status=status.HTTP_200_OK,
                   )
            group_challenge = GroupChallengesModel.objects.filter(id=group_challenge_id).first()
            if not group_challenge:
                   return Response(
                       ResponseData.error("Group challenge id is invalid"),
                       status=status.HTTP_200_OK,
                   )
            is_user_already_a_participant = ParticipantsInGroupChallengeModel.objects.filter(user_id=user_id,group_challenge_id=group_challenge_id,hide_from_user=False).first()
            if is_user_already_a_participant:
                   return Response(
                       ResponseData.error("You are already a participant in this challenge"),
                       status=status.HTTP_200_OK,
                   )
            new_data = ParticipantsInGroupChallengeModel.objects.create(
                user_id=user_id,
                group_challenge_id=group_challenge_id
            )
            new_data.save()
            return Response(
                ResponseData.success_without_data(
                    "New user added in this group challenge successfully"),
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

@api_view(["POST"])
def upload_video_for_group_challenge(request):
    """Function to upload challenge video of a user"""
    try:
        data = request.data
        serializer = UploadVideoOfUserGroupChallengeSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            group_challenge_id = serializer.data["group_challenge_id"]
            video_file = serializer.data['video_file']
            user = UserModel.objects.filter(id=user_id,is_active=True).first()
            if not user:
                   return Response(
                       ResponseData.error("User id is invalid"),
                       status=status.HTTP_200_OK,
                   )
            group_challenge = GroupChallengesModel.objects.filter(id=group_challenge_id).first()
            if not group_challenge:
                   return Response(
                       ResponseData.error("Group challenge id is invalid"),
                       status=status.HTTP_200_OK,
                   )
            user_challenge_data = ParticipantsInGroupChallengeModel.objects.filter(user_id=user_id,group_challenge_id=group_challenge_id,hide_from_user=False).get()
            if user_challenge_data is None:
                return Response(
                       ResponseData.error("You are not a participant yet. Please participate first."),
                       status=status.HTTP_200_OK,
                   )
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

@api_view(["POST"])
def update_user_participation_for_group_challenge(request):
    """Function to update user particiation for group challenge"""
    try:
        data = request.data
        serializer = UpdateUserParticipationStatusInGroupChallengeSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            group_challenge_id = serializer.data["group_challenge_id"]
            want_to_participate = serializer.data['want_to_participate']
            user = UserModel.objects.filter(id=user_id,is_active=True).first()
            if not user:
                   return Response(
                       ResponseData.error("User id is invalid"),
                       status=status.HTTP_200_OK,
                   )
            group_challenge = GroupChallengesModel.objects.filter(id=group_challenge_id).first()
            if not group_challenge:
                   return Response(
                       ResponseData.error("Group challenge id is invalid"),
                       status=status.HTTP_200_OK,
                   )
            user_challenge_data = ParticipantsInGroupChallengeModel.objects.filter(user_id=user_id,group_challenge_id=group_challenge_id).get()
            if user_challenge_data is None:
                return Response(
                       ResponseData.error("You are not a participant yet. Please participate first."),
                       status=status.HTTP_200_OK,
                   )
            if want_to_participate == False:
                user_challenge_data.hide_from_user = True
                user_challenge_data.save()
            else:
                user_challenge_data.hide_from_user = False
                user_challenge_data.save()
            return Response(
                ResponseData.success_without_data(
                    "Status updated successfully"),
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