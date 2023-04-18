from datetime import datetime
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
from user.models import UserHealthDetailsModel, UserModel
from commitment.models import CommitmentCategoryModel, CommitmentModel

# Create your views here.
@api_view(["POST"])
def get_all_group_challenges(request):
    """Function to get group challenges based on date"""
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
            is_finished = serializer.data['is_finished'] 
            is_ongoing = serializer.data['is_ongoing'] 
            is_upcoming = serializer.data['is_upcoming'] 
            sort_by = serializer.data['sort_by']
            age_group = serializer.data['age_group']
            gender = serializer.data['gender']
            min_rating = serializer.data['min_rating']
            max_rating = serializer.data['max_rating']
            # start_date = serializer.data['start_date']
            # end_date = serializer.data['end_date']
            page_number = int(serializer.data['page_no'] if 'page_no' in request.data else 0)
            page_size_param = int(serializer.data['page_size'] if 'page_size' in request.data else 0)
            page_no = page_number
            page_size = page_size_param
            start=(page_no-1)*page_size
            end=page_no*page_size
            if(age_group is not None):
                min_age = str(age_group).split("-")[0]
                max_age = str(age_group).split("-")[1]
            today_date = datetime.now().date()
            if is_finished is not None and age_group is None and gender is not None and min_rating is None:
                challenges_data = GroupChallengesModel.objects.values().filter(end_date__lt=today_date,gender=gender).all()[start:end]
            elif is_finished is not None and age_group is None and gender is not None and min_rating is not None:
                challenges_data = GroupChallengesModel.objects.values().filter(end_date__lt=today_date,gender=gender,min_rating=min_rating,max_rating=max_rating).all()[start:end]
            elif is_finished is not None and age_group is None and min_rating is None:
                challenges_data = GroupChallengesModel.objects.values().filter(end_date__lt=today_date).all()[start:end]
            elif is_finished is not None and age_group is None and min_rating is not None:
                challenges_data = GroupChallengesModel.objects.values().filter(end_date__lt=today_date,min_rating=min_rating,max_rating=max_rating).all()[start:end]
            elif is_finished is not None and age_group is not None and gender is not None and min_rating is None:
                challenges_data = GroupChallengesModel.objects.values().filter(end_date__lt=today_date,min_age__lte=min_age,max_age__gte=max_age,gender=gender).all()[start:end]
            elif is_finished is not None and age_group is not None and gender is not None and min_rating is not None:
                challenges_data = GroupChallengesModel.objects.values().filter(end_date__lt=today_date,min_age__lte=min_age,max_age__gte=max_age,gender=gender,min_rating=min_rating,max_rating=max_rating).all()[start:end]
            elif is_finished is not None and age_group is not None and min_rating is None:
                challenges_data = GroupChallengesModel.objects.values().filter(end_date__lt=today_date,min_age__lte=min_age,max_age__gte=max_age).all()[start:end]
            elif is_finished is not None and age_group is not None and min_rating is not None:
                challenges_data = GroupChallengesModel.objects.values().filter(end_date__lt=today_date,min_age__lte=min_age,max_age__gte=max_age,min_rating=min_rating,max_rating=max_rating).all()[start:end]
            elif is_finished is None and age_group is not None and gender is not None and min_rating is None:
                challenges_data = GroupChallengesModel.objects.values().filter(min_age__lte=min_age,max_age__gte=max_age,gender=gender).all()[start:end]
            elif is_finished is None and age_group is not None and gender is not None and min_rating is not None:
                challenges_data = GroupChallengesModel.objects.values().filter(min_age__lte=min_age,max_age__gte=max_age,gender=gender,min_rating=min_rating,max_rating=max_rating).all()[start:end]
            elif is_finished is None and age_group is not None and min_rating is None:
                challenges_data = GroupChallengesModel.objects.values().filter(min_age__lte=min_age,max_age__gte=max_age).all()[start:end]
            elif is_finished is None and age_group is not None and min_rating is not None:
                challenges_data = GroupChallengesModel.objects.values().filter(min_age__lte=min_age,max_age__gte=max_age,min_rating=min_rating,max_rating=max_rating).all()[start:end]
            elif is_ongoing is not None and age_group is None and gender is not None and min_rating is None:
                challenges_data = GroupChallengesModel.objects.values().filter(start_date__lte=today_date,end_date__gte=today_date,gender=gender).all()[start:end]
            elif is_ongoing is not None and age_group is None and gender is not None and min_rating is not None:
                challenges_data = GroupChallengesModel.objects.values().filter(start_date__lte=today_date,end_date__gte=today_date,gender=gender,min_rating=min_rating,max_rating=max_rating).all()[start:end]
            elif is_ongoing is not None and age_group is None and min_rating is None:
                challenges_data = GroupChallengesModel.objects.values().filter(start_date__lte=today_date,end_date__gte=today_date).all()[start:end]
            elif is_ongoing is not None and age_group is None and min_rating is not None:
                challenges_data = GroupChallengesModel.objects.values().filter(start_date__lte=today_date,end_date__gte=today_date,min_rating=min_rating,max_rating=max_rating).all()[start:end]
            elif is_ongoing is not None and age_group is not None and gender is not None and min_rating is None:
                challenges_data = GroupChallengesModel.objects.values().filter(start_date__lte=today_date,end_date__gte=today_date,min_age__lte=min_age,max_age__gte=max_age,gender=gender).all()[start:end]
            elif is_ongoing is not None and age_group is not None and gender is not None and min_rating is not None:
                challenges_data = GroupChallengesModel.objects.values().filter(start_date__lte=today_date,end_date__gte=today_date,min_age__lte=min_age,max_age__gte=max_age,gender=gender,min_rating=min_rating,max_rating=max_rating).all()[start:end]
            elif is_ongoing is not None and age_group is not None and min_rating is None:
                challenges_data = GroupChallengesModel.objects.values().filter(start_date__lte=today_date,end_date__gte=today_date,min_age__lte=min_age,max_age__gte=max_age).all()[start:end]
            elif is_ongoing is not None and age_group is not None and min_rating is not None:
                challenges_data = GroupChallengesModel.objects.values().filter(start_date__lte=today_date,end_date__gte=today_date,min_age__lte=min_age,max_age__gte=max_age,min_rating=min_rating,max_rating=max_rating).all()[start:end]
            elif is_ongoing is None and age_group is not None and gender is not None and min_rating is None:
                challenges_data = GroupChallengesModel.objects.values().filter(min_age__lte=min_age,max_age__gte=max_age,gender=gender).all()[start:end]
            elif is_ongoing is None and age_group is not None and gender is not None and min_rating is not None:
                challenges_data = GroupChallengesModel.objects.values().filter(min_age__lte=min_age,max_age__gte=max_age,gender=gender,min_rating=min_rating,max_rating=max_rating).all()[start:end]
            elif is_ongoing is None and age_group is not None and min_rating is None:
                challenges_data = GroupChallengesModel.objects.values().filter(min_age__lte=min_age,max_age__gte=max_age).all()[start:end]
            elif is_ongoing is None and age_group is not None and min_rating is not None:
                challenges_data = GroupChallengesModel.objects.values().filter(min_age__lte=min_age,max_age__gte=max_age,min_rating=min_rating,max_rating=max_rating).all()[start:end]
            elif is_upcoming is not None and age_group is None and gender is not None and min_rating is None:
                challenges_data = GroupChallengesModel.objects.values().filter(start_date__gt=today_date,gender=gender).all()[start:end]
            elif is_upcoming is not None and age_group is None and gender is not None and min_rating is not None:
                challenges_data = GroupChallengesModel.objects.values().filter(start_date__gt=today_date,gender=gender,min_rating=min_rating,max_rating=max_rating).all()[start:end]
            elif is_upcoming is not None and age_group is None and min_rating is None:
                challenges_data = GroupChallengesModel.objects.values().filter(start_date__gt=today_date).all()[start:end]
            elif is_upcoming is not None and age_group is None and min_rating is not None:
                challenges_data = GroupChallengesModel.objects.values().filter(start_date__gt=today_date,min_rating=min_rating,max_rating=max_rating).all()[start:end]
            elif is_upcoming is not None and age_group is not None and gender is not None and min_rating is None:
                challenges_data = GroupChallengesModel.objects.values().filter(start_date__gt=today_date,min_age__lte=min_age,max_age__gte=max_age,gender=gender).all()[start:end]
            elif is_upcoming is not None and age_group is not None and gender is not None and min_rating is not None:
                challenges_data = GroupChallengesModel.objects.values().filter(start_date__gt=today_date,min_age__lte=min_age,max_age__gte=max_age,gender=gender,min_rating=min_rating,max_rating=max_rating).all()[start:end]
            elif is_upcoming is not None and age_group is not None and min_rating is None:
                challenges_data = GroupChallengesModel.objects.values().filter(start_date__gt=today_date,min_age__lte=min_age,max_age__gte=max_age).all()[start:end]
            elif is_upcoming is not None and age_group is not None and min_rating is not None:
                challenges_data = GroupChallengesModel.objects.values().filter(start_date__gt=today_date,min_age__lte=min_age,max_age__gte=max_age,min_rating=min_rating,max_rating=max_rating).all()[start:end]
            elif is_upcoming is None and age_group is not None and gender is not None and min_rating is None:
                challenges_data = GroupChallengesModel.objects.values().filter(min_age__lte=min_age,max_age__gte=max_age,gender=gender).all()[start:end]
            elif is_upcoming is None and age_group is not None and gender is not None and min_rating is not None:
                challenges_data = GroupChallengesModel.objects.values().filter(min_age__lte=min_age,max_age__gte=max_age,gender=gender,min_rating=min_rating,max_rating=max_rating).all()[start:end]
            elif is_upcoming is None and age_group is not None and min_rating is None:
                challenges_data = GroupChallengesModel.objects.values().filter(min_age__lte=min_age,max_age__gte=max_age).all()[start:end]
            elif is_upcoming is None and age_group is not None and min_rating is not None:
                challenges_data = GroupChallengesModel.objects.values().filter(min_age__lte=min_age,max_age__gte=max_age,min_rating=min_rating,max_rating=max_rating).all()[start:end]
            elif gender is not None and min_rating is None:
                challenges_data = GroupChallengesModel.objects.values().filter(gender=gender).all()[start:end]
            elif gender is not None and min_rating is not None:
                challenges_data = GroupChallengesModel.objects.values().filter(gender=gender,min_rating=min_rating,max_rating=max_rating).all()[start:end]
            elif gender is None and min_rating is not None:
                challenges_data = GroupChallengesModel.objects.values().filter(min_rating=min_rating,max_rating=max_rating).all()[start:end]
            else:
                challenges_data = GroupChallengesModel.objects.values().all()[start:end]
            if len(challenges_data) == 0:
                    return Response(
                       ResponseData.success(
                           [], "No group challenge found"),
                       status=status.HTTP_201_CREATED)
            for i in range(0,len(challenges_data)):
                user_age = UserHealthDetailsModel.objects.filter(user_id=user_id).first().age
                user_gender = UserHealthDetailsModel.objects.filter(user_id=user_id).first().gender
                user_rating = 0
                total_commitments_of_user = CommitmentModel.objects.filter(user_id=user_id).count()
                total_done_commitments_of_user = CommitmentModel.objects.filter(user_id=user_id,is_done=True,is_updated=True).count()
                if (total_commitments_of_user) != 0:
                   user_rating = (total_done_commitments_of_user/total_commitments_of_user)*100
                else:
                   user_rating = 0
                challenges_data[i]['is_user_between_this_age'] = False
                challenges_data[i]['is_user_rating_between_this_competition_rating'] = False
                challenges_data[i]['is_participation_allowed'] = False
                challenges_data[i]['is_past_competition'] = False
                challenges_data[i]['is_future_competition'] = False
                if(user_age>=challenges_data[i]['min_age'] and user_age<=challenges_data[i]['max_age']):
                    challenges_data[i]['is_user_between_this_age'] = True
                if(user_rating>=challenges_data[i]['min_rating'] and user_rating<=challenges_data[i]['max_rating']):
                    challenges_data[i]['is_user_rating_between_this_competition_rating'] = True
                if(challenges_data[i]['start_date'] <= today_date and challenges_data[i]['end_date'] >= today_date and challenges_data[i]['gender'].lower() ==  user_gender.lower()):
                    challenges_data[i]['is_participation_allowed'] = True
                if(challenges_data[i]['end_date'] < today_date ):
                    challenges_data[i]['is_past_competition'] = True
                if(challenges_data[i]['start_date'] > today_date ):
                    challenges_data[i]['is_future_competition'] = True
                challenges_data[i]['challenge_rules'] = RulesOfGroupChallengeModel.objects.values().filter().all()
                for j in range(0,len(challenges_data[i]['challenge_rules'])):
                    challenges_data[i]['challenge_rules'][j].pop('created_at')
                    challenges_data[i]['challenge_rules'][j].pop('updated_at')
                challenges_data[i]['challenge_guidelines'] = GuidelinesOfGroupChallengeModel.objects.values().filter().all()
                for j in range(0,len(challenges_data[i]['challenge_guidelines'])):
                    challenges_data[i]['challenge_guidelines'][j].pop('created_at')
                    challenges_data[i]['challenge_guidelines'][j].pop('updated_at')
                    challenges_data[i]['challenge_guidelines'][j].pop('group_challenge_id')
                challenges_data[i]['is_user_participating'] = False
                challenges_data[i]['has_user_submitted_video'] = False
                challenges_data[i]['challenge_video'] = ''
                print(challenges_data[i]['id'])
                is_user_participant = ParticipantsInGroupChallengeModel.objects.filter(user_id=user_id,group_challenge_id=challenges_data[i]['id']).first()
                if is_user_participant is not None:
                    challenges_data[i]['is_user_participating'] = True
                    challenges_data[i]['has_user_submitted_video'] = is_user_participant.has_submitted_video
                    challenges_data[i]['challenge_video'] = f"{is_user_participant.challenge_video}"
                challenges_data[i]['total_participants'] = len(ParticipantsInGroupChallengeModel.objects.filter(group_challenge_id=challenges_data[i]['id']).all())
                challenges_data[i]['total_videos_submitted'] = len(ParticipantsInGroupChallengeModel.objects.filter(group_challenge_id=challenges_data[i]['id'],has_submitted_video=True).all())
                if is_user_participant is not None:
                    challenges_data[i]['is_user_participating'] = True
            if(sort_by is not None):
                if(sort_by == 'Latest to Oldest'):
                    challenges_data = sorted(challenges_data, key=lambda d: d['created_at'],reverse=True)
                elif(sort_by == 'Oldest to Latest'):
                    challenges_data = sorted(challenges_data, key=lambda d: d['created_at'])
                elif(sort_by == 'Max to min participants'):
                    challenges_data = sorted(challenges_data, key=lambda d: d['total_participants'],reverse=True)
                elif(sort_by == 'Min to max participants'):
                    challenges_data = sorted(challenges_data, key=lambda d: d['total_participants'])           
            for i in range(0,len(challenges_data)):
                challenges_data[i].pop('created_at')
                challenges_data[i].pop('updated_at')
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
def get_user_group_challenges(request):
    """Function to get group challenges in which user has participated"""
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
            is_ongoing = serializer.data['is_ongoing'] 
            is_finished = serializer.data['is_finished'] 
            sort_by = serializer.data['sort_by']
            page_number = int(serializer.data['page_no'] if 'page_no' in request.data else 0)
            page_size_param = int(serializer.data['page_size'] if 'page_size' in request.data else 0)
            page_no = page_number
            page_size = page_size_param
            start=(page_no-1)*page_size
            end=page_no*page_size
            today_date = datetime.now().date()
            final_list = []
            if is_ongoing is not None:
                total_challenges_data = ParticipantsInGroupChallengeModel.objects.values().filter(user_id=user_id,
                group_challenge__start_date__lte=today_date,group_challenge__end_date__gte=today_date).all()[start:end]
            elif is_finished is not None:
                total_challenges_data = ParticipantsInGroupChallengeModel.objects.values().filter(user_id=user_id,
                group_challenge__end_date__lt=today_date).all()[start:end]
            else:
                total_challenges_data = ParticipantsInGroupChallengeModel.objects.values().filter(user_id=user_id).all()[start:end]
            for i in range(0,len(total_challenges_data)):
                if is_ongoing is not None:
                    challenges_data = GroupChallengesModel.objects.values().filter(id=total_challenges_data[i]["group_challenge_id"],start_date__lte=today_date,end_date__gte=today_date).get()
                elif is_finished is not None:
                    challenges_data = GroupChallengesModel.objects.values().filter(id=total_challenges_data[i]["group_challenge_id"],end_date__lt=today_date).get()
                else:
                    challenges_data = GroupChallengesModel.objects.values().filter(id=total_challenges_data[i]["group_challenge_id"],).get()
                challenges_data['is_past_competition'] = False
                challenges_data['is_future_competition'] = False
                if(challenges_data['end_date'] < today_date ):
                    challenges_data['is_past_competition'] = True
                if(challenges_data['start_date'] > today_date ):
                    challenges_data['is_future_competition'] = True
                challenges_data['challenge_rules'] = RulesOfGroupChallengeModel.objects.values().filter().all()
                for j in range(0,len(challenges_data['challenge_rules'])):
                    challenges_data['challenge_rules'][j].pop('created_at')
                    challenges_data['challenge_rules'][j].pop('updated_at')
                challenges_data['challenge_guidelines'] = GuidelinesOfGroupChallengeModel.objects.values().filter().all()
                for j in range(0,len(challenges_data['challenge_guidelines'])):
                    challenges_data['challenge_guidelines'][j].pop('created_at')
                    challenges_data['challenge_guidelines'][j].pop('updated_at')
                    challenges_data['challenge_guidelines'][j].pop('group_challenge_id')
                challenges_data['has_user_submitted_video'] = False
                is_user_participant = ParticipantsInGroupChallengeModel.objects.filter(user_id=user_id,group_challenge_id=challenges_data['id']).first()
                if is_user_participant is not None:
                    challenges_data['is_user_participating'] = True
                    challenges_data['has_user_submitted_video'] = is_user_participant.has_submitted_video
                challenges_data['total_participants'] = len(ParticipantsInGroupChallengeModel.objects.filter(group_challenge_id=challenges_data['id']).all())
                challenges_data['total_videos_submitted'] = len(ParticipantsInGroupChallengeModel.objects.filter(group_challenge_id=challenges_data['id'],has_submitted_video=True).all())
                if is_user_participant is not None:
                    challenges_data['is_user_participating'] = True
                final_list.append(challenges_data)
            if(sort_by is not None):
                if(sort_by == 'Latest to Oldest'):
                    final_list = sorted(final_list, key=lambda d: d['created_at'],reverse=True)
                elif(sort_by == 'Oldest to Latest'):
                    final_list = sorted(final_list, key=lambda d: d['created_at'])
                elif(sort_by == 'Max to min participants'):
                    final_list = sorted(final_list, key=lambda d: d['total_participants'],reverse=True)
                elif(sort_by == 'Min to max participants'):
                    final_list = sorted(final_list, key=lambda d: d['total_participants']) 
            for i in range(0,len(final_list)):           
                final_list[i].pop('created_at')
                final_list[i].pop('updated_at')
            return Response(
                       ResponseData.success(
                           final_list, "User Challenges fetched successfully"),
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
        print(f"data {data}")
        serializer = UploadVideoOfUserGroupChallengeSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            group_challenge_id = serializer.data["group_challenge_id"]
            video_file = request.FILES['video_file']
            is_updated_file = request.data["is_updated_file"]
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