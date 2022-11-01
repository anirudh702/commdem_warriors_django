from datetime import datetime, timedelta
from django.shortcuts import render
from rest_framework.decorators import api_view
from commitment import serializers
from commitment.models import CauseOfCategorySuccessOrFailureModel, CommitmentModel,CommitmentCategoryModel,CommitmentNameModel, ReasonBehindCommitmentSuccessOrFailureForUser
from rest_framework.response import Response
from commitment.serializers import AddCauseOfCategorySerializer, AddCommitmentSerializer,AddCommitmentCategorySerializer,AddCommitmentNameSerializer, GetCauseOfCategorySerializer, GetCommitmentCategorySerializer, GetCommitmentNameSerializer, GetCommitmentsSerializer, UpdateCommitmentsSerializer
from django.core.files.storage import FileSystemStorage
from response import Response as ResponseData
from rest_framework import status
from django.http.response import JsonResponse

from user.models import UserModel
from django.core.cache import cache

# Create your views here.

@api_view(["POST"])
def add_new_commitment(request):
    """Function to add new commitment"""
    try:
        data = request.data
        user_id = request.data["user"]
        commitment_category_id_with_name_id = request.data['category_id_with_name_id']
        user = UserModel.objects.filter(id=user_id).first()
        if not user:
            return Response(
                ResponseData.error("User id is invalid"),
                status=status.HTTP_200_OK,
            )
        final_data = []
        for i in range(0,len(str(commitment_category_id_with_name_id).split(','))):
            both = str(commitment_category_id_with_name_id).split(',')[i].split(':')
            category_id = both[0]
            commitment_name_id = both[1]
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
            commitment_category_data = CommitmentModel.objects.filter(user=UserModel(id=user_id),category_id=category_id).all()
            print(f"commitment_category_data {commitment_category_data}")
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
            final_data.append(CommitmentModel(
                user=UserModel(id=user_id),
                # commitment_date=datetime.now() + timedelta(days=1),
                category=CommitmentCategoryModel(id=category_id),
                commitment_name=CommitmentNameModel(id=commitment_name_id),
                ))
        CommitmentModel.objects.bulk_create(final_data)
        # new_commitment = CommitmentModel.objects.create(
        #     user=UserModel(id=user_id),
        #     category=CommitmentCategoryModel(id=category_id),
        #     commitment_name=CommitmentNameModel(id=commitment_name_id),
        # )
        # new_commitment.save()
        # commitment_details = list(
        #     CommitmentModel.objects.values().filter(id=new_commitment.id))
        return Response(
            ResponseData.success_without_data(
                 "Commitment added successfully"),
            status=status.HTTP_201_CREATED,
        )
        # for error in serializer.errors:
        #     print(serializer.errors[error][0])
        # return Response(
        #     ResponseData.error(serializer.errors[error][0]),
        #     status=status.HTTP_400_BAD_REQUEST,
        # )
        return Response(
                    ResponseData.error(serializer.errors),
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
def add_cause_of_category_success_or_failure(request):
    """Function to add cause of category failure or success"""
    try:
        data = request.data
        serializer = AddCauseOfCategorySerializer(data=data)
        if serializer.is_valid():
            category_id = serializer.data["category"]
            title = serializer.data["title"]
            is_success = serializer.data['is_success']
            category = CommitmentCategoryModel.objects.filter(id=category_id).first()
            if not category:
                return Response(
                    ResponseData.error("Category id is invalid"),
                    status=status.HTTP_200_OK,
                )
            data_exist_or_not = CauseOfCategorySuccessOrFailureModel.objects.filter(category=CommitmentCategoryModel(id=category_id),title=title).first()
            if data_exist_or_not:
                return Response(
                    ResponseData.error("This data already exists"),
                    status=status.HTTP_200_OK,
                )
            new_cause_of_category = CauseOfCategorySuccessOrFailureModel.objects.create(
                category = CommitmentCategoryModel(id=category_id),
                title = title,
                is_success = is_success
            )
            new_cause_of_category.save()
            return Response(
                ResponseData.success(
                    [], "Cause of category success/failure added successfully"),
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
def get_cause_of_category_success_or_failure(request):
    """Function to get cause of category success or failure data"""
    try:
        data = request.data
        serializer = GetCauseOfCategorySerializer(data=data)
        if serializer.is_valid():
            print("dscdscdscs")
            category_id = serializer.data['category']
            is_success = serializer.data['is_success']
            category = CommitmentCategoryModel.objects.filter(id=category_id).first()
            print(f"categorcdcdy {category}")
            if not category:
                return Response(
                    ResponseData.error("Category id is invalid"),
                    status=status.HTTP_200_OK,
                )
            cause_of_category_data = CauseOfCategorySuccessOrFailureModel.objects.filter(category = CommitmentCategoryModel(id=category_id)).first()
            if not cause_of_category_data:
                return Response(
                    ResponseData.error("Cause of category id is invalid"),
                    status=status.HTTP_200_OK,
                )
            cause_of_category = CauseOfCategorySuccessOrFailureModel.objects.values().filter(
            category = CommitmentCategoryModel(id=category_id),is_success=is_success).all()
            for i in range(0,len(cause_of_category)):
                cause_of_category[i]['isSelected'] = False
                cause_of_category[i].pop('created_at')
                cause_of_category[i].pop('updated_at')
            return Response(
                ResponseData.success(
                    cause_of_category, "Cause of category data fetched successfully"),
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
def get_commitment_category_with_name(request):
    """Function to get commitment category with name"""
    try:
        data = request.data
        serializer = GetCommitmentCategorySerializer(data=data)
        if serializer.is_valid():
            category_id = serializer.data["id"]
            if category_id is None:
                commitment_category_data = list(
                CommitmentCategoryModel.objects.values().filter())
                for i in range(0,len(commitment_category_data)):
                    commitment_category_data[i]['commitment_category_name_data'] = list(
                CommitmentNameModel.objects.values().filter(category=CommitmentCategoryModel(id=commitment_category_data[i]['id'])))
                    for j in range(0,len(commitment_category_data[i]['commitment_category_name_data'])):
                        commitment_category_data[i]['commitment_category_name_data'][j].pop('created_at')
                        commitment_category_data[i]['commitment_category_name_data'][j].pop('updated_at')
                        commitment_category_data[i]['commitment_category_name_data'][j]['isSelected'] = False
                    commitment_category_data[i].pop('created_at')
                    commitment_category_data[i].pop('updated_at')
                return Response(
                    ResponseData.success(
                        commitment_category_data, "Commitment categories fetched successfully"),
                    status=status.HTTP_201_CREATED)
            else:
                commitment_category_data = list(CommitmentCategoryModel.objects.values().filter(id=category_id).get())
                commitment_category_data[0]['commitment_category_name_data'] = list(
                CommitmentNameModel.objects.values().filter(category=CommitmentCategoryModel(id=category_id)))
                for j in range(0,len(commitment_category_data[0]['commitment_category_name_data'])):
                        commitment_category_data[0]['commitment_category_name_data'][j].pop('created_at')
                        commitment_category_data[0]['commitment_category_name_data'][j].pop('updated_at')
                        commitment_category_data[i]['commitment_category_name_data'][j]['isSelected'] = False
                commitment_category_data[0].pop('created_at')
                commitment_category_data[0].pop('updated_at')
                return Response(
                    ResponseData.success(
                        commitment_category_data, "Commitment category fetched successfully"),
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
def get_commitment_name(request):
    """Function to get commitment name"""
    try:
        data = request.data
        serializer = GetCommitmentNameSerializer(data=data)
        if serializer.is_valid():
            category_id = serializer.data["category"]
            if category_id is None:
                commitment_name_data = list(
                CommitmentNameModel.objects.values().filter())
                for i in range(0,len(commitment_name_data)):
                    commitment_name_data[i].pop('created_at')
                    commitment_name_data[i].pop('updated_at')
                return Response(
                    ResponseData.success(
                        commitment_name_data, "Commitment names fetched successfully"),
                    status=status.HTTP_201_CREATED)
            else:
                commitment_name_data = CommitmentNameModel.objects.values().filter(category = CommitmentCategoryModel(id=category_id)).all()
                for i in range(0,len(commitment_name_data)):
                    commitment_name_data[i].pop('created_at')
                    commitment_name_data[i].pop('updated_at')
                return Response(
                    ResponseData.success(
                        commitment_name_data, "Commitment name fetched successfully"),
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
def get_all_commitments(request):
    """Function to get user commitments"""
    try:
        data = request.data
        serializer = GetCommitmentsSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user"]
            cache_key = ""     
            #        cache_key = "get_commitment_commitment_data" if user_id is None else f"get_commitment_commitment_data_{user_id}"
            #        data = cache.get(cache_key)
            #        if data:
            #           return Response(
            #            ResponseData.success(
            #                data, "Commitments fetched successfully"),
            #            status=status.HTTP_201_CREATED)
            commitment_data = []
            commitment_data = list(
                CommitmentModel.objects.values().filter())
            if len(commitment_data) == 0:
                       return Response(
                       ResponseData.success(
                           [], "No commitment found"),
                       status=status.HTTP_201_CREATED)
            for i in range(0,len(commitment_data)):
                commitment_data[i].pop('created_at')
                commitment_data[i].pop('updated_at')
                commitment_data[i].pop('user_id')
                commitment_data[i]['category_data'] = CommitmentCategoryModel.objects.values().filter(id=commitment_data[i]['category_id']).get()
                commitment_data[i].pop('category_id')
                commitment_data[i]['category_data'].pop('created_at')
                commitment_data[i]['category_data'].pop('updated_at')
                commitment_data[i]['commitment_name_data'] = CommitmentNameModel.objects.values().filter(id=commitment_data[i]['commitment_name_id']).get()
                commitment_data[i]['reasons_behind_success_or_failure'] = ReasonBehindCommitmentSuccessOrFailureForUser.objects.values().filter(
                    user=UserModel(id=user_id),commitment=CommitmentModel(id=commitment_data[i]['id'])).all()
                for j in range(0,len(commitment_data[i]['reasons_behind_success_or_failure'])):
                    commitment_data[i]['reasons_behind_success_or_failure'][j]['cause_data'] = CauseOfCategorySuccessOrFailureModel.objects.values().filter(id=
                    commitment_data[i]['reasons_behind_success_or_failure'][j]['cause_of_category_success_or_failure_id']).get()
                    commitment_data[i]['reasons_behind_success_or_failure'][j].pop('created_at')
                    commitment_data[i]['reasons_behind_success_or_failure'][j].pop('updated_at')
                    commitment_data[i]['reasons_behind_success_or_failure'][j]['cause_data'].pop('created_at')
                    commitment_data[i]['reasons_behind_success_or_failure'][j]['cause_data'].pop('updated_at')
                    commitment_data[i]['reasons_behind_success_or_failure'][j].pop('cause_of_category_success_or_failure_id')
                commitment_data[i].pop('commitment_name_id')
                commitment_data[i]['commitment_name_data'].pop('created_at')
                commitment_data[i]['commitment_name_data'].pop('updated_at')
            return Response(
                       ResponseData.success(
                           commitment_data, "Commitments fetched successfully"),
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
def get_user_commitments(request):
    """Function to get user commitments"""
    try:
        data = request.data
        user = UserModel.objects.filter(id=request.data['user']).first()
        if not user:
                   return Response(
                       ResponseData.error("User id is invalid"),
                       status=status.HTTP_200_OK,
                   )
        serializer = GetCommitmentsSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user"]
            cache_key = ""     
            cache_key = "get_commitment_data" if user_id is None else f"get_commitment_data_{user_id}"
            data = cache.get(cache_key)
            if data:
               return Response(
                ResponseData.success(
                    data, "Commitments fetched successfully"),
                status=status.HTTP_201_CREATED)
            print("dvdvdf")
            commitment_data = []
            commitment_data = list(
                CommitmentModel.objects.values().filter(user=UserModel(id=user_id)))
            if len(commitment_data) == 0:
                       return Response(
                       ResponseData.success(
                           [], "No commitment found"),
                       status=status.HTTP_201_CREATED)
            for i in range(0,len(commitment_data)):
                commitment_data[i].pop('created_at')
                commitment_data[i].pop('updated_at')
                commitment_data[i].pop('user_id')
                commitment_data[i]['category_data'] = CommitmentCategoryModel.objects.values().filter(id=commitment_data[i]['category_id']).get()
                commitment_data[i].pop('category_id')
                commitment_data[i]['category_data'].pop('created_at')
                commitment_data[i]['category_data'].pop('updated_at')
                commitment_data[i]['commitment_name_data'] = CommitmentNameModel.objects.values().filter(id=commitment_data[i]['commitment_name_id']).get()
                commitment_data[i]['reasons_behind_success_or_failure'] = ReasonBehindCommitmentSuccessOrFailureForUser.objects.values().filter(
                    user=UserModel(id=user_id),commitment=CommitmentModel(id=commitment_data[i]['id'])).all()
                for j in range(0,len(commitment_data[i]['reasons_behind_success_or_failure'])):
                    commitment_data[i]['reasons_behind_success_or_failure'][j]['cause_data'] = CauseOfCategorySuccessOrFailureModel.objects.values().filter(id=
                    commitment_data[i]['reasons_behind_success_or_failure'][j]['cause_of_category_success_or_failure_id']).get()
                    commitment_data[i]['reasons_behind_success_or_failure'][j].pop('created_at')
                    commitment_data[i]['reasons_behind_success_or_failure'][j].pop('updated_at')
                    commitment_data[i]['reasons_behind_success_or_failure'][j]['cause_data'].pop('created_at')
                    commitment_data[i]['reasons_behind_success_or_failure'][j]['cause_data'].pop('updated_at')
                    commitment_data[i]['reasons_behind_success_or_failure'][j].pop('cause_of_category_success_or_failure_id')
                commitment_data[i].pop('commitment_name_id')
                commitment_data[i]['commitment_name_data'].pop('created_at')
                commitment_data[i]['commitment_name_data'].pop('updated_at')
            cache.set(cache_key, commitment_data,timeout=10)
            return Response(
                       ResponseData.success(
                           commitment_data, "Commitments fetched successfully"),
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
def get_user_commitments_by_commitment_date_only(request):
    """Function to get user commitments based on commitment date only"""
    try:
        data = request.data
        user = UserModel.objects.filter(id=request.data['user']).first()
        if not user:
                   return Response(
                       ResponseData.error("User id is invalid"),
                       status=status.HTTP_200_OK,
                   )
        serializer = GetCommitmentsSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user"]
            commitment_date = serializer.data['commitment_date']
            # cache_key = ""     
            # cache_key = f"get_commitment_{str(commitment_date).split('T')[0]}" if user_id is None else f"get_commitment_{str(commitment_date).split('T')[0]}_{user_id}"
            # data = cache.get(cache_key)
            # if data:
            #    return Response(
            #     ResponseData.success(
            #         data, "Commitments fetched successfully"),
            #     status=status.HTTP_201_CREATED)
            commitment_data = []
            commitment_data = list(
                CommitmentModel.objects.values().filter(user=UserModel(id=user_id)))
            if len(commitment_data) == 0:
                       return Response(
                       ResponseData.success(
                           [], "No commitment found"),
                       status=status.HTTP_201_CREATED)
            commitment_filtered_data = []
            for i in range(0,len(commitment_data)):
                commitment_data[i].pop('created_at')
                commitment_data[i].pop('updated_at')
                commitment_data[i].pop('user_id')
                commitment_data[i]['category_data'] = CommitmentCategoryModel.objects.values().filter(id=commitment_data[i]['category_id']).get()
                commitment_data[i].pop('category_id')
                commitment_data[i]['category_data'].pop('created_at')
                commitment_data[i]['category_data'].pop('updated_at')
                commitment_data[i]['commitment_name_data'] = CommitmentNameModel.objects.values().filter(id=commitment_data[i]['commitment_name_id']).get()
                commitment_data[i]['reasons_behind_success_or_failure'] = ReasonBehindCommitmentSuccessOrFailureForUser.objects.values().filter(
                    user=UserModel(id=user_id),commitment=CommitmentModel(id=commitment_data[i]['id'])).all()
                for j in range(0,len(commitment_data[i]['reasons_behind_success_or_failure'])):
                    commitment_data[i]['reasons_behind_success_or_failure'][j]['cause_data'] = CauseOfCategorySuccessOrFailureModel.objects.values().filter(id=
                    commitment_data[i]['reasons_behind_success_or_failure'][j]['cause_of_category_success_or_failure_id']).get()
                    commitment_data[i]['reasons_behind_success_or_failure'][j].pop('created_at')
                    commitment_data[i]['reasons_behind_success_or_failure'][j].pop('updated_at')
                    commitment_data[i]['reasons_behind_success_or_failure'][j]['cause_data'].pop('created_at')
                    commitment_data[i]['reasons_behind_success_or_failure'][j]['cause_data'].pop('updated_at')
                    commitment_data[i]['reasons_behind_success_or_failure'][j].pop('cause_of_category_success_or_failure_id')
                commitment_data[i].pop('commitment_name_id')
                commitment_data[i]['commitment_name_data'].pop('created_at')
                commitment_data[i]['commitment_name_data'].pop('updated_at')
            # cache.set(cache_key, commitment_data)
            for i in range(0,len(commitment_data)):
                     if str(commitment_data[i]['commitment_date']).split(" ")[0] == str(commitment_date).split("T")[0]:
                        commitment_filtered_data.append(commitment_data[i])
            if len(commitment_filtered_data) == 0:
                       return Response(
                       ResponseData.success(
                           [], "No commitment found"),
                       status=status.HTTP_201_CREATED)
            # cache.set(cache_key, commitment_filtered_data,timeout=5)
            return Response(
                       ResponseData.success(
                           commitment_filtered_data, "Commitments fetched successfully"),
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
def get_user_commitments_by_start_end_date_only(request):
    """Function to get user commitments based on start and end date only"""
    try:
        data = request.data
        user = UserModel.objects.filter(id=request.data['user']).first()
        if not user:
                   return Response(
                       ResponseData.error("User id is invalid"),
                       status=status.HTTP_200_OK,
                   )
        serializer = GetCommitmentsSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user"]
            start_date = serializer.data['start_date']
            end_date = serializer.data['end_date']
            cache_key = ""     
            #        cache_key = f"get_commitment_{str(start_date).split('T')[0]}_{str(start_date).split('T')[0]}" if user_id is None else f"get_commitment_{str(start_date).split('T')[0]}_{str(start_date).split('T')[0]}_{user_id}"
            #        data = cache.get(cache_key)
            #        print(f"data {data}")
            #        if data:
            #           return Response(
            #            ResponseData.success(
            #                data, "Commitments fetched successfully"),
            #            status=status.HTTP_201_CREATED)
            commitment_data = []
            commitment_data = list(
            CommitmentModel.objects.values().filter(user=UserModel(id=user_id)))
            if len(commitment_data) == 0:
                       return Response(
                       ResponseData.success(
                           [], "No commitment found"),
                       status=status.HTTP_201_CREATED)
            commitment_filtered_data = []
            for i in range(0,len(commitment_data)):
                commitment_data[i].pop('created_at')
                commitment_data[i].pop('updated_at')
                commitment_data[i].pop('user_id')
                commitment_data[i]['category_data'] = CommitmentCategoryModel.objects.values().filter(id=commitment_data[i]['category_id']).get()
                commitment_data[i].pop('category_id')
                commitment_data[i]['category_data'].pop('created_at')
                commitment_data[i]['category_data'].pop('updated_at')
                commitment_data[i]['commitment_name_data'] = CommitmentNameModel.objects.values().filter(id=commitment_data[i]['commitment_name_id']).get()
                commitment_data[i]['reasons_behind_success_or_failure'] = ReasonBehindCommitmentSuccessOrFailureForUser.objects.values().filter(
                    user=UserModel(id=user_id),commitment=CommitmentModel(id=commitment_data[i]['id'])).all()
                for j in range(0,len(commitment_data[i]['reasons_behind_success_or_failure'])):
                    commitment_data[i]['reasons_behind_success_or_failure'][j]['cause_data'] = CauseOfCategorySuccessOrFailureModel.objects.values().filter(id=
                    commitment_data[i]['reasons_behind_success_or_failure'][j]['cause_of_category_success_or_failure_id']).get()
                    commitment_data[i]['reasons_behind_success_or_failure'][j].pop('created_at')
                    commitment_data[i]['reasons_behind_success_or_failure'][j].pop('updated_at')
                    commitment_data[i]['reasons_behind_success_or_failure'][j]['cause_data'].pop('created_at')
                    commitment_data[i]['reasons_behind_success_or_failure'][j]['cause_data'].pop('updated_at')
                    commitment_data[i]['reasons_behind_success_or_failure'][j].pop('cause_of_category_success_or_failure_id')
                commitment_data[i].pop('commitment_name_id')
                commitment_data[i]['commitment_name_data'].pop('created_at')
                commitment_data[i]['commitment_name_data'].pop('updated_at')
            for i in range(0,len(commitment_data)):
              sub_start_date = datetime.strptime(str(start_date).split("T")[0], "%Y-%m-%d").date()
              sub_end_date = datetime.strptime(str(end_date).split("T")[0], "%Y-%m-%d").date()
              current_date = datetime.strptime(str(commitment_data[i]['commitment_date']).split(" ")[0], "%Y-%m-%d").date()
              if current_date >= sub_start_date and current_date <= sub_end_date:
                 commitment_filtered_data.append(commitment_data[i])
            if len(commitment_filtered_data) == 0:
                return Response(
                ResponseData.success(
                    [], "No commitment found"),
                status=status.HTTP_201_CREATED)
            cache.set(cache_key, commitment_filtered_data)
            return Response(
                ResponseData.success(
                    commitment_filtered_data, "Commitments fetched successfully"),
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
def update_commitment(request):
    """Function to update commitment based on user id and commitment id"""
    try:
        data = request.data
        user = UserModel.objects.filter(id=request.data['user']).first()
        if not user:
                return Response(
                    ResponseData.error("User id is invalid"),
                    status=status.HTTP_200_OK,
                )
        commitment_id = CommitmentModel.objects.filter(id=request.data['id']).first()
        if not commitment_id:
                return Response(
                    ResponseData.error("Commitment id is invalid"),
                    status=status.HTTP_200_OK,
                )
        serializer = UpdateCommitmentsSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user"]
            commitment_id = serializer.data['id']
            cause_id = serializer.data['cause_id']
            is_done = serializer.data['is_done']
            commitment_data = CommitmentModel.objects.filter(
                id=commitment_id,user=UserModel(id=user_id)
            ).first()
            commitment_data.is_done = is_done
            commitment_data.is_updated = True
            commitment_data.save()
            cause_ids = str(cause_id).replace("[","").replace("]","").split(":")
            print(f"cause_ids {cause_ids}")
            for i in range(0,len(cause_ids)):
                print(f"cause_ids[i] {cause_ids[i]}")
                if cause_ids[i] != "":
                   cause_id = CauseOfCategorySuccessOrFailureModel.objects.filter(id=int(cause_ids[i])).first()
                   if not cause_id:
                           return Response(
                               ResponseData.error("Any one of the cause id is invalid"),
                               status=status.HTTP_200_OK,
                           )
                   reasons = ReasonBehindCommitmentSuccessOrFailureForUser.objects.create(
                       user = UserModel(id=user_id),
                       commitment = CommitmentModel(id=commitment_id),
                       cause_of_category_success_or_failure = CauseOfCategorySuccessOrFailureModel(id=int(cause_ids[i]))
                   )
                   reasons.save()
            return Response(
                ResponseData.success_without_data("Commitment updated successfully"),
                status=status.HTTP_201_CREATED)
        return Response(
                    ResponseData.error(serializer.errors),
                    status=status.HTTP_400_BAD_REQUEST,
                )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

