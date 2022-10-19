from datetime import datetime, timedelta
from django.shortcuts import render
from rest_framework.decorators import api_view
from commitment.models import CommitmentModel,CommitmentCategoryModel,CommitmentNameModel
from rest_framework.response import Response
from commitment.serializers import AddCommitmentSerializer,AddCommitmentCategorySerializer,AddCommitmentNameSerializer, GetCommitmentCategorySerializer, GetCommitmentNameSerializer, GetCommitmentsSerializer
from django.core.files.storage import FileSystemStorage
from response import Response as ResponseData
from rest_framework import status
from django.http.response import JsonResponse

from user.models import UserModel

# Create your views here.

@api_view(["POST"])
def add_new_commitment(request):
    """Function to add new commitment"""
    try:
        data = request.data
        serializer = AddCommitmentSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user"]
            category_id = serializer.data["category"]
            commitment_name_id = serializer.data["commitment_name"]
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response(
                    ResponseData.error("User id is invalid"),
                    status=status.HTTP_200_OK,
                )
            category = CommitmentCategoryModel.objects.filter(id=category_id).first()
            if not category:
                return Response(
                    ResponseData.error("Category id is invalid"),
                    status=status.HTTP_200_OK,
                )
            commitment_name = CommitmentNameModel.objects.filter(id=commitment_name_id).first()
            if not commitment_name:
                return Response(
                    ResponseData.error("Commitment name id is invalid"),
                    status=status.HTTP_200_OK,
                )
            commitment_category_data = CommitmentModel.objects.filter(category_id=category_id).all()
            already_exists = False
            for i in range(0,len(commitment_category_data)):
                if str(commitment_category_data[i].commitment_date).__contains__(str(datetime.now() + timedelta(days=1)).split(' ')[0]) or str(commitment_category_data[i].commitment_date).__contains__(str(datetime.now()).split(' ')[0]):
                    already_exists = True
                    break
            if already_exists:
                return Response(
                    ResponseData.error("Commitment already exists with same category for day specified"),
                    status=status.HTTP_200_OK,
                )
            new_commitment = CommitmentModel.objects.create(
                user=UserModel(id=user_id),
                category=CommitmentCategoryModel(id=category_id),
                commitment_name=CommitmentNameModel(id=commitment_name_id),
            )
            new_commitment.save()
            commitment_details = list(
                CommitmentModel.objects.values().filter(id=new_commitment.id))
            return Response(
                ResponseData.success(
                    commitment_details[0], "Commitment for a user added successfully"),
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
def add_new_commitment_category(request):
    """Function to add new commitment category"""
    try:
        data = request.data
        serializer = AddCommitmentCategorySerializer(data=data)
        if serializer.is_valid():
            name = serializer.data["name"]
            new_commitment_category = CommitmentCategoryModel.objects.create(
                name=name,
            )
            new_commitment_category.save()
            return Response(
                ResponseData.success(
                    [], "Commitment category added successfully"),
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
def add_new_commitment_name(request):
    """Function to add new commitment name"""
    try:
        data = request.data
        serializer = AddCommitmentNameSerializer(data=data)
        if serializer.is_valid():
            name = serializer.data["name"]
            category_id = serializer.data['category']
            category = CommitmentCategoryModel.objects.filter(id=category_id).first()
            if not category:
                return Response(
                    ResponseData.error("Category id is invalid"),
                    status=status.HTTP_200_OK,
                )
            new_commitment_name = CommitmentNameModel.objects.create(
                name=name,
                category=CommitmentCategoryModel(id=category_id)
            )
            new_commitment_name.save()
            return Response(
                ResponseData.success(
                    [], "Commitment name added successfully"),
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
def get_commitment_category(request):
    """Function to get commitment category"""
    try:
        data = request.data
        serializer = GetCommitmentCategorySerializer(data=data)
        if serializer.is_valid():
            category_id = serializer.data["id"]
            if category_id is None:
                commitment_category_data = list(
                CommitmentCategoryModel.objects.values().filter())
                return Response(
                    ResponseData.success(
                        commitment_category_data, "Commitment categories fetched successfully"),
                    status=status.HTTP_201_CREATED)
            else:
                commitment_category_data = CommitmentCategoryModel.objects.values().filter(id=category_id).get()
                return Response(
                    ResponseData.success(
                        commitment_category_data, "Commitment category fetched successfully"),
                    status=status.HTTP_201_CREATED)
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["POST"])
def get_commitment_name(request):
    """Function to get commitment name"""
    try:
        data = request.data
        serializer = GetCommitmentNameSerializer(data=data)
        if serializer.is_valid():
            name_id = serializer.data["id"]
            if name_id is None:
                commitment_name_data = list(
                CommitmentNameModel.objects.values().filter())
                return Response(
                    ResponseData.success(
                        commitment_name_data, "Commitment names fetched successfully"),
                    status=status.HTTP_201_CREATED)
            else:
                commitment_name_data = CommitmentNameModel.objects.values().filter(id=name_id).get()
                return Response(
                    ResponseData.success(
                        commitment_name_data, "Commitment name fetched successfully"),
                    status=status.HTTP_201_CREATED)
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["POST"])
def get_commitments(request):
    """Function to get commitments"""
    try:
        data = request.data
        serializer = GetCommitmentsSerializer(data=data)
        if serializer.is_valid():
            commitment_id = serializer.data["id"]
            if commitment_id is None:
                commitment_data = list(
                CommitmentModel.objects.values().filter())
                for i in range(0,len(commitment_data)):
                    commitment_data[i]['user_data'] = UserModel.objects.values().filter(id=commitment_data[i]['user_id']).get()
                    commitment_data[i].pop('user_id')
                    commitment_data[i]['category_data'] = CommitmentCategoryModel.objects.values().filter(id=commitment_data[i]['category_id']).get()
                    commitment_data[i].pop('category_id')
                    commitment_data[i]['commitment_name_data'] = CommitmentNameModel.objects.values().filter(id=commitment_data[i]['commitment_name_id']).get()
                    commitment_data[i].pop('commitment_name_id')
                return Response(
                    ResponseData.success(
                        commitment_data, "Commitments fetched successfully"),
                    status=status.HTTP_201_CREATED)
            else:
                commitment_data = dict(CommitmentModel.objects.values().filter(id=commitment_id).get())
                commitment_data['user_data'] = UserModel.objects.values().filter(id=commitment_data['user_id']).get()
                commitment_data.pop('user_id')
                commitment_data['category_data'] = CommitmentCategoryModel.objects.values().filter(id=commitment_data['category_id']).get()
                commitment_data.pop('category_id')
                commitment_data['commitment_name_data'] = CommitmentNameModel.objects.values().filter(id=commitment_data['commitment_name_id']).get()
                commitment_data.pop('commitment_name_id')
                return Response(
                    ResponseData.success(
                        commitment_data, "Commitment fetched successfully"),
                    status=status.HTTP_201_CREATED)
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )