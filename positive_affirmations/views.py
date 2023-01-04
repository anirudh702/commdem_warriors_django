from datetime import *
from django.shortcuts import render
from rest_framework.decorators import api_view
from positive_affirmations.models import PositiveAffirmationModel, UserAffirmationModel
from positive_affirmations.serializers import GetPositiveAffirmationsSerializer, UpdateUserPositiveAffirmationsSerializer
from rest_framework.response import Response
from response import Response as ResponseData
from rest_framework import status

@api_view(["POST"])
def getPositiveAffirmations(request):
    """Function to get all designations"""
    affirmations_data = PositiveAffirmationModel.objects.values().filter().all()
    for i in range(0,len(affirmations_data)):
        affirmations_data[i].pop('created_at')
        affirmations_data[i].pop('updated_at')
    return Response(
        ResponseData.success(
            affirmations_data, "Affirmation details fetched successfully"),
        status=status.HTTP_201_CREATED)

@api_view(["POST"])
def updateUserPositiveAffirmationStatus(request):
    """Function to update status of positive affirmation of a user"""
    try:
        data = request.data
        serializer = UpdateUserPositiveAffirmationsSerializer(data=data)
        if serializer.is_valid():
          user_id = serializer.data['user_id']
          number_of_commitment_for_week_id = serializer.data['number_of_commitment_for_week_id']
          affirmations_data = UserAffirmationModel.objects.filter(
              user_id=user_id,
              number_of_commitment_for_week_id=number_of_commitment_for_week_id
              ).first()
          affirmations_data.did_user_speak = True
          affirmations_data.updated_at = datetime.now()
          affirmations_data.save()
          return Response(
              ResponseData.success_without_data(
                  "Affirmation details updated successfully"),
              status=status.HTTP_201_CREATED)
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