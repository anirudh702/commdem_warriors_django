import os
from django.forms import model_to_dict
from django.shortcuts import render
from googletrans import Translator
import gtts
import calendar
from rest_framework.decorators import api_view
from workout.models import WorkoutModel
from workout.serializers import GetWorkoutdataSerializer
from location.models import CitiesModel
from commitment.models import CauseOfCategorySuccessOrFailureModel, CommitmentModel,CommitmentCategoryModel,CommitmentNameModel, ExerciseModel, ReasonBehindCommitmentSuccessOrFailureForUser, UserCommitmentsForNextWeekModel, next_weekday
from rest_framework.response import Response
from commitment.serializers import AddCauseOfCategorySerializer,AddCommitmentCategorySerializer,AddCommitmentNameSerializer, AddUserNumberOfCommitmentsFornextWeekSerializer, GetCauseOfCategorySerializer, GetCommitmentCategorySerializer, GetCommitmentNameSerializer, GetCommitmentsSerializer, GetOtherUsersCommitmentsSerializer, GetUserCommitmentsForCurrentWeekSerializer, UpdateCommitmentsSerializer
from designation.models import DesignationModel
from income.models import IncomeModel
from positive_affirmations.models import UserAffirmationModel
from response import Response as ResponseData
from rest_framework import status
from subscription.models import SubscriptionLevelModel, SubscriptionModel
from user.models import UserLocationDetailsModel, UserModel, UserPaymentDetailsModel, UserProfessionalDetailsModel, UserSubscriptionDetailsModel, keysToUpdateInFrontEndModel
from django.db.models import Q
from datetime import *

from voiceAssistant.models import userPreferredVoiceLanguageModel, voiceAssistantAfterUpdateMessageModel

# Create your views here.
@api_view(["POST"])
def get_workout_of_today_of_user(request):
    """Function to get workout for user of that day"""
    try:
        data = request.data
        print(f"data {data}")
        user = UserModel.objects.filter(id=request.data['user_id'],is_active=True).first()
        if not user:
                   return Response(
                       ResponseData.error("User id is invalid"),
                       status=status.HTTP_200_OK,
                   )
        serializer = GetWorkoutdataSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            todays_date = str(datetime.now()).split(" ")[0]
            commitment_data = CommitmentModel.objects.values().filter(user_id=user_id,category_id=3).filter(Q(commitment_date__icontains=todays_date)).first()
            print(f"dssscs {commitment_data}")
            if commitment_data is None:
                workout_data = WorkoutModel.objects.values().filter(level_of_workout_id=4).order_by('level_of_workout_id').all()
            else:
               print(f"commitment_data {commitment_data['commitment_name_id']}")
               workout_data = WorkoutModel.objects.values().filter(
                workout_name_id=commitment_data['commitment_name_id']
                ).order_by('level_of_workout_id').all()
            print(f"workout_data {workout_data}")
            for i in range(0,len(workout_data)):
                workout_data[i].pop('created_at')
                workout_data[i].pop('updated_at')
            return Response(
                ResponseData.success(
                    workout_data, "Commitments fetched successfully"),
                status=status.HTTP_201_CREATED)
        return Response(
                    ResponseData.error(serializer.errors),
                    status=status.HTTP_400_BAD_REQUEST,
                )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )