from datetime import datetime, timedelta
from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework.decorators import api_view
from location.models import CitiesModel
from commitment.models import CauseOfCategorySuccessOrFailureModel, CommitmentModel,CommitmentCategoryModel,CommitmentNameModel, ReasonBehindCommitmentSuccessOrFailureForUser
from rest_framework.response import Response
from commitment.serializers import AddCauseOfCategorySerializer,AddCommitmentCategorySerializer,AddCommitmentNameSerializer, GetCauseOfCategorySerializer, GetCommitmentCategorySerializer, GetCommitmentNameSerializer, GetCommitmentsSerializer, GetOtherUsersCommitmentsSerializer, UpdateCommitmentsSerializer
from designation.models import DesignationModel
from income.models import IncomeModel
from response import Response as ResponseData
from rest_framework import status
from user.models import UserLocationDetailsModel, UserModel, UserProfessionalDetailsModel
from django.db.models import Q

# Create your views here.
# UserRouter().create_user_materialized_view()

@api_view(["POST"])
def add_new_commitment(request):
    """Function to add new commitment"""
    try:
        user_id = request.data["user_id"]
        commitment_category_id_with_name_id = request.data['category_id_with_name_id']
        user = UserModel.objects.using('user_db').filter(id=user_id,is_active=True).first()
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
            category = CommitmentCategoryModel.objects.using('commitment_db').filter(id=category_id).first()
            if not category:
                return Response(
                    ResponseData.error("Category id is invalid"),
                    status=status.HTTP_200_OK,
                )
            commitment_name = CommitmentNameModel.objects.using('commitment_db').filter(id=commitment_name_id).first()
            if not commitment_name:
                return Response(
                    ResponseData.error("Commitment name id is invalid"),
                    status=status.HTTP_200_OK,
                )
            commitment_category_data = CommitmentModel.objects.using('commitment_db').filter(user_id=user_id,category_id=category_id).all()
            print(f"commitment_category_data {commitment_category_data}")
            already_exists = False
            for i in range(0,commitment_category_data.count()):
                if str(commitment_category_data[i].commitment_date).__contains__(str(datetime.now() + timedelta(days=0)).split(' ')[0]):
                    already_exists = True
                    break
            if already_exists:
                return Response(
                    ResponseData.error("Commitment already exists with same category for day specified"),
                    status=status.HTTP_201_CREATED,
                )
            final_data.append(CommitmentModel(
                user_id=user_id,
                commitment_date=datetime.now() + timedelta(days=0),
                category=CommitmentCategoryModel(id=category_id),
                commitment_name=CommitmentNameModel(id=commitment_name_id),
                ))
        CommitmentModel.objects.using('commitment_db').bulk_create(final_data)
        return Response(
            ResponseData.success_without_data(
                 "Commitment added successfully"),
            status=status.HTTP_201_CREATED,
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
            new_commitment_category = CommitmentCategoryModel.objects.using('commitment_db').create(
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
            category = CommitmentCategoryModel.objects.using('commitment_db').filter(id=category_id).first()
            if not category:
                return Response(
                    ResponseData.error("Category id is invalid"),
                    status=status.HTTP_200_OK,
                )
            data_exist_or_not = CauseOfCategorySuccessOrFailureModel.objects.using('commitment_db').filter(category=CommitmentCategoryModel(id=category_id),title=title).first()
            if data_exist_or_not:
                return Response(
                    ResponseData.error("This data already exists"),
                    status=status.HTTP_200_OK,
                )
            new_cause_of_category = CauseOfCategorySuccessOrFailureModel.objects.using('commitment_db').create(
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
            category_id = serializer.data['category']
            is_success = serializer.data['is_success']
            category = CommitmentCategoryModel.objects.using('commitment_db').filter(id=category_id).first()
            if(category_id == 2 or category_id == 3):
                evening_time = '19:00:00'
                evening_time_format = datetime.strptime(evening_time, '%H:%M:%S')
                if(datetime.now().time() < evening_time_format.time()):
                   return Response(
                    ResponseData.error("You can update this commitment post 7 pm"),
                    status=status.HTTP_200_OK,
                )
            if not category:
                return Response(
                    ResponseData.error("Category id is invalid"),
                    status=status.HTTP_200_OK,
                )
            cause_of_category_data = CauseOfCategorySuccessOrFailureModel.objects.using('commitment_db').filter(category = CommitmentCategoryModel(id=category_id)).first()
            if not cause_of_category_data:
                return Response(
                    ResponseData.error("Cause of category id is invalid"),
                    status=status.HTTP_200_OK,
                )
            cause_of_category = CauseOfCategorySuccessOrFailureModel.objects.using('commitment_db').values().filter(
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
            success_name = serializer.data["successName"]
            failure_name = serializer.data["failureName"]
            current_day_name = serializer.data["currentDayName"]
            category_id = serializer.data['category']
            category = CommitmentCategoryModel.objects.using('commitment_db').filter(id=category_id).first()
            if not category:
                return Response(
                    ResponseData.error("Category id is invalid"),
                    status=status.HTTP_200_OK,
                )
            new_commitment_name = CommitmentNameModel.objects.using('commitment_db').create(
                name=name,
                successName=success_name,
                failureName=failure_name,
                currentDayName=current_day_name,
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
                CommitmentCategoryModel.objects.using('commitment_db').values().filter())
                for i in range(0,len(commitment_category_data)):
                    commitment_category_data[i]['commitment_category_name_data'] = list(
                CommitmentNameModel.objects.using('commitment_db').values().filter(category=CommitmentCategoryModel(id=commitment_category_data[i]['id'])))
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
                commitment_category_data = list(CommitmentCategoryModel.objects.using('commitment_db').values().filter(id=category_id).get())
                commitment_category_data[0]['commitment_category_name_data'] = list(
                CommitmentNameModel.objects.using('commitment_db').values().filter(category=CommitmentCategoryModel(id=category_id)))
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
                CommitmentNameModel.objects.using('commitment_db').values().filter())
                for i in range(0,commitment_name_data.count()):
                    commitment_name_data[i].pop('created_at')
                    commitment_name_data[i].pop('updated_at')
                return Response(
                    ResponseData.success(
                        commitment_name_data, "Commitment names fetched successfully"),
                    status=status.HTTP_201_CREATED)
            else:
                commitment_name_data = CommitmentNameModel.objects.using('commitment_db').values().filter(category = CommitmentCategoryModel(id=category_id)).all()
                for i in range(0,commitment_name_data.count()):
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

def functionForReasonsBehindCommitments(commitment_data,i):
        commitment_data[i].pop('commitment_name_id')
        commitment_data[i]['commitment_name_data'].pop('created_at')
        commitment_data[i]['commitment_name_data'].pop('updated_at')
        for j in range(0,len(commitment_data[i]['reasons_behind_success_or_failure'])):
                commitment_data[i]['reasons_behind_success_or_failure'][j]['cause_data'] = CauseOfCategorySuccessOrFailureModel.objects.using('commitment_db').values().filter(id=
                commitment_data[i]['reasons_behind_success_or_failure'][j]['cause_of_category_success_or_failure_id']).get()
                commitment_data[i]['reasons_behind_success_or_failure'][j].pop('created_at')
                commitment_data[i]['reasons_behind_success_or_failure'][j].pop('updated_at')
                if(commitment_data[i]['reasons_behind_success_or_failure'][j]['cause_data'] is not None):
                   commitment_data[i]['reasons_behind_success_or_failure'][j]['cause_data'].pop('created_at')
                   commitment_data[i]['reasons_behind_success_or_failure'][j]['cause_data'].pop('updated_at')
                commitment_data[i]['reasons_behind_success_or_failure'][j].pop('cause_of_category_success_or_failure_id')


def changesInAllCommitment(commitment_data,user_id):
    for i in range(0,len(commitment_data)):
        commitment_data[i].pop('created_at')
        commitment_data[i].pop('updated_at')
        commitment_data[i].pop('user_id')
        commitment_data[i]['category_data'] = CommitmentCategoryModel.objects.using('commitment_db').values().filter(id=commitment_data[i]['category_id']).get()
        commitment_data[i].pop('category_id')
        commitment_data[i]['category_data'].pop('created_at')
        commitment_data[i]['category_data'].pop('updated_at')
        commitment_data[i]['commitment_name_data'] = CommitmentNameModel.objects.using('commitment_db').values().filter(id=commitment_data[i]['commitment_name_id']).get()
        commitment_data[i]['reasons_behind_success_or_failure'] = ReasonBehindCommitmentSuccessOrFailureForUser.objects.values().filter(
           user_id=user_id,commitment=CommitmentModel(id=commitment_data[i]['id'])).all()
        functionForReasonsBehindCommitments(commitment_data,i)
    return commitment_data

def changesInOtherCommitments(commitment_data):
        for i in range(0,len(commitment_data)):
            commitment_data[i].pop('created_at')
            commitment_data[i].pop('updated_at')
            commitment_data[i]['user_data'] = UserModel.objects.using('user_db').values().filter(id=commitment_data[i]['user_id']).first()
            city = UserLocationDetailsModel.objects.using('user_db').values().filter(user_id=commitment_data[i]['user_id']).first()
            if city is not None:
               commitment_data[i]['user_data']['city_data'] = CitiesModel.objects.using('location_db').values().filter(id=city['city_id']).first()
               commitment_data[i]['user_data']['city_data'].pop('created_at')
               commitment_data[i]['user_data']['city_data'].pop('updated_at')
            income_range_id = UserProfessionalDetailsModel.objects.values().using('user_db').filter(user_id=commitment_data[i]['user_id']).first()
            if income_range_id is not None:
               commitment_data[i]['user_data']['income_range_data'] = IncomeModel.objects.using('income_db').values().filter(id=income_range_id['income_range_id']).get()
               commitment_data[i]['user_data']['income_range_data'].pop('created_at')
               commitment_data[i]['user_data']['income_range_data'].pop('updated_at')
            designation = UserProfessionalDetailsModel.objects.using('user_db').values().filter(user_id=commitment_data[i]['user_id']).first()
            if designation is not None:
               commitment_data[i]['user_data']['designation_data'] = DesignationModel.objects.using('designation_db').values().filter(id=designation['designation_id']).get()
               commitment_data[i]['user_data']['designation_data'].pop('created_at')
               commitment_data[i]['user_data']['designation_data'].pop('updated_at')
            commitment_data[i]['user_data'].pop('created_at')
            commitment_data[i]['user_data'].pop('updated_at')
            commitment_data[i]['category_data'] = CommitmentCategoryModel.objects.using('commitment_db').values().filter(id=commitment_data[i]['category_id']).get()
            commitment_data[i].pop('category_id')
            commitment_data[i]['category_data'].pop('created_at')
            commitment_data[i]['category_data'].pop('updated_at')
            commitment_data[i]['commitment_name_data'] = CommitmentNameModel.objects.using('commitment_db').values().filter(id=commitment_data[i]['commitment_name_id']).get()
            commitment_data[i]['reasons_behind_success_or_failure'] = ReasonBehindCommitmentSuccessOrFailureForUser.objects.using('commitment_db').values().filter(
                user_id=commitment_data[i]['user_id'],commitment=CommitmentModel(id=commitment_data[i]['id'])).all()
            commitment_data[i].pop('user_id')
            functionForReasonsBehindCommitments(commitment_data,i)
        return commitment_data

@api_view(["POST"])
def get_all_commitments(request):
    """Function to get user commitments"""
    try:
        data = request.data
        serializer = GetCommitmentsSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            commitment_data = []
            commitment_data = list(
                CommitmentModel.objects.using('commitment_db').values().filter().order_by('-commitment_date'))
            if commitment_data.count() == 0:
                       return Response(
                       ResponseData.success(
                           [], "No commitment found"),
                       status=status.HTTP_201_CREATED)
            final_commitment_data = changesInAllCommitment(commitment_data,user_id)
            return Response(
                       ResponseData.success(
                           final_commitment_data, "Commitments fetched successfully"),
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
def get_other_users_commitments(request):
    """Function to get other users commitments"""
    try:
        request_data = request.data
        print(f"request_data {request_data}")
        page_number = int(request_data['page_no'] if 'page_no' in request.data else 0)
        page_size_param = int(request_data['page_size'] if 'page_size' in request.data else 0)
        search_param = request_data['search_param'] if 'search_param' in request.data else ""
        page_no = page_number
        page_size = page_size_param
        start=(page_no-1)*page_size
        end=page_no*page_size
        print(start)
        print(end)
        print(page_number)
        print(search_param)
        commitment_data = []
        if page_number == 0 and search_param != "":
            commitment_data = CommitmentModel.objects.using('commitment_db').values().filter().order_by('-commitment_date')
        elif page_number != 0 and search_param != "":
            commitment_data = CommitmentModel.objects.using('commitment_db').values().filter().order_by('-commitment_date')[start:end]
        elif page_number != 0 and search_param == "":
            commitment_data = CommitmentModel.objects.using('commitment_db').values().filter().order_by('-commitment_date')[start:end]
        else:
            commitment_data = CommitmentModel.objects.using('commitment_db').values().filter().order_by('-commitment_date')
        final_commitment_data = []
        if commitment_data is None:
                   return Response(
                   ResponseData.success(
                       [], "No commitment found"),
                   status=status.HTTP_201_CREATED)
        final_data = changesInOtherCommitments(commitment_data)
        if search_param != "":
          print("called")
          for i in range(0,len(final_data)):
            one_item = final_data[i]
            print(one_item)
            if(str(one_item['user_data']['full_name']).__contains__(search_param) or 
            str(one_item['user_data']['mobile_number']).__contains__(search_param)
            or str(one_item['category_data']['name']).__contains__(search_param)):
                final_commitment_data.append(one_item)
        else:
            final_commitment_data = final_data
        if len(final_commitment_data) == 0:
                   return Response(
                   ResponseData.success(
                       [], "No commitment found"),
                   status=status.HTTP_201_CREATED)
        return Response(
                   ResponseData.success(
                       final_commitment_data, "Commitments fetched successfully"),
                   status=status.HTTP_201_CREATED)
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["POST"])
def get_group_commitments_by_commitment_date_only(request):
    """Function to get group commitments based on commitment date only"""
    try:
        data = request.data
        print(data)
        user = UserModel.objects.using('user_db').filter(id=request.data['user_id'],is_active=True).first()
        if not user:
                   return Response(
                       ResponseData.error("User id is invalid"),
                       status=status.HTTP_200_OK,
                   )
        serializer = GetCommitmentsSerializer(data=data)
        if serializer.is_valid():
            commitment_date = serializer.data['commitment_date']
            page_number = int(serializer.data['page_no'] if 'page_no' in request.data else 0)
            page_size_param = int(serializer.data['page_size'] if 'page_size' in request.data else 0)
            search_param = serializer.data['search_param'] if 'search_param' in request.data else ""
            page_no = page_number
            page_size = page_size_param
            start=(page_no-1)*page_size
            end=page_no*page_size
            commitment_data = []
            if page_number == 0 and search_param != "":
                commitment_data = CommitmentModel.objects.using('commitment_db').values().filter(Q(commitment_date__icontains=commitment_date) & (Q(category__name__icontains=search_param))).order_by('-commitment_date')
            elif page_number != 0 and search_param != "":
                commitment_data = CommitmentModel.objects.using('commitment_db').values().filter(Q(commitment_date__icontains=commitment_date) & (Q(category__name__icontains=search_param))).order_by('-commitment_date')[start:end]
            elif page_number != 0 and search_param == "":
                commitment_data = CommitmentModel.objects.using('commitment_db').values().filter(Q(commitment_date__icontains=commitment_date)).order_by('-commitment_date')[start:end]
            else:
                commitment_data = CommitmentModel.objects.using('commitment_db').values().filter(Q(commitment_date__icontains=commitment_date)).order_by('-commitment_date')
            if commitment_data.count() == 0:
                    return Response(
                       ResponseData.success(
                           [], "No commitment found"),
                       status=status.HTTP_201_CREATED)
            return Response(
                       ResponseData.success(
                           changesInOtherCommitments(commitment_data), "Commitments fetched successfully"),
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
        print(data)
        user = UserModel.objects.using('user_db').filter(id=request.data['user_id'],is_active=True).first()
        if not user:
                   return Response(
                       ResponseData.error("User id is invalid"),
                       status=status.HTTP_200_OK,
                   )
        serializer = GetCommitmentsSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            page_number = int(serializer.data['page_no'] if 'page_no' in request.data else 0)
            page_size_param = int(serializer.data['page_size'] if 'page_size' in request.data else 0)
            search_param = serializer.data['search_param'] if 'search_param' in request.data else ""
            page_no = page_number
            page_size = page_size_param
            start=(page_no-1)*page_size
            end=page_no*page_size
            commitment_data = []
            if page_number == 0 and search_param != "":
                commitment_data =CommitmentModel.objects.using('commitment_db').values().filter(user_id=user_id).filter(Q(category__name__icontains=search_param)).order_by('-commitment_date')
            elif page_number != 0 and search_param != "":
                commitment_data = CommitmentModel.objects.using('commitment_db').values().filter(user_id=user_id).filter(Q(category__name__icontains=search_param)).order_by('-commitment_date')[start:end]
            elif page_number != 0 and search_param == "":
                commitment_data = CommitmentModel.objects.using('commitment_db').values().filter(user_id=user_id).filter().order_by('-commitment_date')[start:end]
            else:
                commitment_data = CommitmentModel.objects.using('commitment_db').values().filter(user_id=user_id).filter().order_by('-commitment_date')
            if commitment_data.count() == 0:
                       return Response(
                       ResponseData.success(
                           [], "No commitment found"),
                       status=status.HTTP_201_CREATED)
            return Response(
                       ResponseData.success(
                           changesInAllCommitment(commitment_data,user_id), "Commitments fetched successfully"),
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
        print(data)
        user = UserModel.objects.using('user_db').filter(id=request.data['user_id'],is_active=True).first()
        if not user:
                   return Response(
                       ResponseData.error("User id is invalid"),
                       status=status.HTTP_200_OK,
                   )
        serializer = GetCommitmentsSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            commitment_date = serializer.data['commitment_date']
            page_number = int(serializer.data['page_no'] if 'page_no' in request.data else 0)
            page_size_param = int(serializer.data['page_size'] if 'page_size' in request.data else 0)
            search_param = serializer.data['search_param'] if 'search_param' in request.data else ""
            page_no = page_number
            page_size = page_size_param
            start=(page_no-1)*page_size
            end=page_no*page_size
            commitment_data = []
            print("Dcd")
            if page_number == 0 and search_param != "":
                commitment_data = CommitmentModel.objects.using('commitment_db').values().filter(user_id=user_id).filter(Q(commitment_date__icontains=commitment_date) & (Q(category__name__icontains=search_param))).order_by('-commitment_date')
            elif page_number != 0 and search_param != "":
                commitment_data = CommitmentModel.objects.using('commitment_db').values().filter(user_id=user_id).filter(Q(commitment_date__icontains=commitment_date) & (Q(category__name__icontains=search_param))).order_by('-commitment_date')[start:end]
            elif page_number != 0 and search_param == "":
                commitment_data = CommitmentModel.objects.using('commitment_db').values().filter(user_id=user_id).filter(Q(commitment_date__icontains=commitment_date)).order_by('-commitment_date')[start:end]
            else:
                commitment_data = CommitmentModel.objects.using('commitment_db').values().filter(user_id=user_id).filter(Q(commitment_date__icontains=commitment_date)).order_by('-commitment_date')
            if commitment_data.count() == 0:
                       return Response(
                       ResponseData.success(
                           [], "No commitment found"),
                       status=status.HTTP_201_CREATED)
            final_data = changesInAllCommitment(commitment_data,user_id)
            return Response(
                       ResponseData.success(
                           final_data, "Commitments fetched successfully"),
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
def share_user_commitment_on_whatsapp(request):
    """Function to share user's commitments on whatsapp """
    try:
        data = request.data
        print(data)
        user = UserModel.objects.using('user_db').filter(id=request.data['user_id'],is_active=True).first()
        if not user:
                   return Response(
                       ResponseData.error("User id is invalid"),
                       status=status.HTTP_200_OK,
                   )
        serializer = GetCommitmentsSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            title_message = serializer.data['title_message']
            commitment_date = serializer.data['commitment_date']
            finalMessage = f"{title_message}\n\n"
            commitment_data = CommitmentModel.objects.using('commitment_db').values().filter(user_id=user_id).filter(Q(commitment_date__icontains=commitment_date)).order_by('-commitment_date').all()
            if commitment_data.count() == 0:
                       return Response(
                       ResponseData.success_without_data(
                           "No commitment found"),
                       status=status.HTTP_201_CREATED)
            isPending = False
            message = ""
            for i in range(0,len(commitment_data)):
                   commitment_data[i]['category_data'] = CommitmentCategoryModel.objects.using('commitment_db').values().filter(id=commitment_data[i]['category_id']).get()
                   finalMessage += f"{i+1}. {commitment_data[i]['category_data']['name']}\n"
                   commitment_data[i]['commitment_name_data'] = CommitmentNameModel.objects.using('commitment_db').values().filter(id=commitment_data[i]['commitment_name_id']).get()
                   if(commitment_data[i]['commitment_date'].date() > datetime.now().date()):
                    finalMessage += f"-> {commitment_data[i]['commitment_name_data']['name']}\n"
                   else:
                    if(commitment_data[i]['is_done'] and commitment_data[i]['is_updated']):
                       finalMessage += f"-> {commitment_data[i]['commitment_name_data']['successName']}\n"
                    elif(commitment_data[i]['is_done'] == False and commitment_data[i]['is_updated']):
                       finalMessage += f"-> {commitment_data[i]['commitment_name_data']['failureName']}\n"
                    else:
                        message += f"{commitment_data[i]['category_data']['name']},"
                        isPending = True
            if isPending:
                return Response(
                           ResponseData.success_without_data(
                           f"Status of commitment {message} is pending"),
                           status=status.HTTP_201_CREATED)
            return Response(
                       ResponseData.success(
                           finalMessage, "Whatsapp message fetched successfully"),
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
        user = UserModel.objects.using('user_db').filter(id=request.data['user_id'],is_active=True).first()
        if not user:
                   return Response(
                       ResponseData.error("User id is invalid"),
                       status=status.HTTP_200_OK,
                   )
        serializer = GetCommitmentsSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            start_date = serializer.data['start_date']
            end_date = serializer.data['end_date']
            cache_key = "" 
            page_number = int(serializer.data['page_no'] if 'page_no' in request.data else 0)
            page_size_param = int(serializer.data['page_size'] if 'page_size' in request.data else 0)
            search_param = serializer.data['search_param'] if 'search_param' in request.data else ""
            page_no = page_number
            page_size = page_size_param
            start=(page_no-1)*page_size
            end=page_no*page_size
            commitment_data = []
            if page_number == 0 and search_param != "":
                commitment_data = CommitmentModel.objects.using('commitment_db').values().filter(user_id=user_id).filter(Q(commitment_date__range=[start_date, end_date]) & (Q(category__name__icontains=search_param))).order_by('-commitment_date')
            elif page_number != 0 and search_param != "":
                commitment_data = CommitmentModel.objects.using('commitment_db').values().filter(user_id=user_id).filter(Q(commitment_date__range=[start_date, end_date]) & (Q(category__name__icontains=search_param))).order_by('-commitment_date')[start:end]
            elif page_number != 0 and search_param == "":
                commitment_data = CommitmentModel.objects.using('commitment_db').values().filter(user_id=user_id).filter(Q(commitment_date__range=[start_date, end_date])).order_by('-commitment_date')[start:end]
            else:
                commitment_data = CommitmentModel.objects.using('commitment_db').values().filter(user_id=user_id).filter(Q(commitment_date__range=[start_date, end_date])).order_by('-commitment_date')
            if commitment_data.count() == 0:
                       return Response(
                       ResponseData.success(
                           [], "No commitment found"),
                       status=status.HTTP_201_CREATED)
            return Response(
                ResponseData.success(
                    changesInAllCommitment(commitment_data,user_id), "Commitments fetched successfully"),
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
def get_group_commitments_by_start_end_date_only(request):
    """Function to get group commitments based on start and end date only"""
    try:
        data = request.data
        user = UserModel.objects.using('user_db').filter(id=request.data['user_id'],is_active=True).first()
        if not user:
                   return Response(
                       ResponseData.error("User id is invalid"),
                       status=status.HTTP_200_OK,
                   )
        serializer = GetCommitmentsSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            start_date = serializer.data['start_date']
            end_date = serializer.data['end_date']
            cache_key = ""    
            page_number = int(serializer.data['page_no'] if 'page_no' in request.data else 0)
            page_size_param = int(serializer.data['page_size'] if 'page_size' in request.data else 0)
            search_param = serializer.data['search_param'] if 'search_param' in request.data else ""
            page_no = page_number
            page_size = page_size_param
            start=(page_no-1)*page_size
            end=page_no*page_size
            commitment_data = []
            if page_number == 0 and search_param != "":
                commitment_data = CommitmentModel.objects.using('commitment_db').values().filter(Q(commitment_date__range=[start_date, end_date]) & (Q(user__last_name__icontains=search_param) | Q(category__name__icontains=search_param))).order_by('-commitment_date')
            elif page_number != 0 and search_param != "":
                commitment_data = CommitmentModel.objects.using('commitment_db').values().filter(Q(commitment_date__range=[start_date, end_date]) & (Q(user__last_name__icontains=search_param) | Q(category__name__icontains=search_param))).order_by('-commitment_date')[start:end]
            elif page_number != 0 and search_param == "":
                commitment_data = CommitmentModel.objects.using('commitment_db').values().filter(Q(commitment_date__range=[start_date, end_date])).order_by('-commitment_date')[start:end]
            else:
                commitment_data = CommitmentModel.objects.using('commitment_db').values().filter(Q(commitment_date__range=[start_date, end_date])).order_by('-commitment_date')
            if commitment_data.count() == 0:
                       return Response(
                       ResponseData.success(
                           [], "No commitment found"),
                       status=status.HTTP_201_CREATED)
            return Response(
                ResponseData.success(
                    changesInOtherCommitments(commitment_data), "Commitments fetched successfully"),
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
        user = UserModel.objects.using('user_db').filter(id=request.data['user_id'],is_active=True).first()
        if not user:
                return Response(
                    ResponseData.error("User id is invalid"),
                    status=status.HTTP_200_OK,
                )
        commitment_id = CommitmentModel.objects.using('commitment_db').filter(id=request.data['id']).first()
        if not commitment_id:
                return Response(
                    ResponseData.error("Commitment id is invalid"),
                    status=status.HTTP_200_OK,
                )
        serializer = UpdateCommitmentsSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            commitment_id = serializer.data['id']
            cause_id = serializer.data['cause_id']
            is_done = serializer.data['is_done']
            commitment_data = CommitmentModel.objects.using('commitment_db').filter(
                id=commitment_id,user_id=user_id
            ).first()
            commitment_data.is_done = is_done
            commitment_data.is_updated = True
            commitment_data.save()
            cause_ids = str(cause_id).replace("[","").replace("]","").split(":")
            print(f"cause_ids {cause_ids}")
            for i in range(0,len(cause_ids)):
                if cause_ids[i] != "":
                   new_ids = str(cause_ids[i]).replace(",","").strip()
                   print(f"cause_ids[i] {new_ids}")
                   cause_id = CauseOfCategorySuccessOrFailureModel.objects.using('commitment_db').filter(id=int(new_ids)).first()
                   if not cause_id:
                           return Response(
                               ResponseData.error("Any one of the cause id is invalid"),
                               status=status.HTTP_200_OK,
                           )
                   does_data_exists_or_not = ReasonBehindCommitmentSuccessOrFailureForUser.objects.using('commitment_db').filter(user_id=user_id,
                   cause_of_category_success_or_failure=CauseOfCategorySuccessOrFailureModel(id=new_ids)).first()
                   if not does_data_exists_or_not:
                       reasons = ReasonBehindCommitmentSuccessOrFailureForUser.objects.using('commitment_db').create(
                           user_id =user_id,
                           commitment = CommitmentModel(id=commitment_id),
                           cause_of_category_success_or_failure = CauseOfCategorySuccessOrFailureModel(id=int(new_ids))
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

