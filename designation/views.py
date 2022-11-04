from django.shortcuts import render
from rest_framework.decorators import api_view
from designation.models import DesignationModel
from designation.serializers import AddDesignationSerializer, GetAllDesignationSerializer
from subscription.models import SubscriptionModel
from rest_framework.response import Response
from response import Response as ResponseData
from rest_framework import status

@api_view(["POST"])
def addNewDesignation(request):
    """Function to add new designation"""
    try:
        data = request.data
        serializer = AddDesignationSerializer(data=data)
        if serializer.is_valid():
            title = str(serializer.data["title"]).lower()
            designation_exists = DesignationModel.objects.filter(title=str(title).lower()).first()
            if designation_exists:
                return Response(
                    ResponseData.error(
                        "This designation already exists"),
                    status=status.HTTP_201_CREATED,
                )
            new_designation = DesignationModel.objects.create(
                title=title
            )
            new_designation.save()
            return Response(
                ResponseData.success_without_data(
                    "Designation added successfully"),
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
def getAllDeisgnations(request):
    """Function to get all designations"""
    try:
        data = request.data
        serializer = GetAllDesignationSerializer(data=data)
        if serializer.is_valid():
            designation_data = DesignationModel.objects.values().filter().all()
            for i in range(0,len(designation_data)):
                designation_data[i].pop('created_at')
                designation_data[i].pop('updated_at')
            return Response(
                ResponseData.success(
                    designation_data, "Designation details fetched successfully"),
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