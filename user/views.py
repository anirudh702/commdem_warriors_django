from django.shortcuts import render
from rest_framework.decorators import api_view
from commitment.models import CommitmentCategoryModel, CommitmentModel
from designation.models import DesignationModel
from subscription.models import SubscriptionModel
from user.models import UserModel, UserPaymentDetailsModel, UserSubscriptionDetailsModel
from rest_framework.response import Response
from user.serializers import AddNewPaymentSerializer, AddUserSubscriptionSerializer, GetAllUsersDetailsSerializer, GetUserProfileSerializer, GetUserSubscriptionSerializer, UserSignInSerializer, UserSignUpSerializer, UserSubscribedOrNotSerializer
from django.core.files.storage import FileSystemStorage
from response import Response as ResponseData
from rest_framework import status
from django.http.response import JsonResponse
from datetime import *

# Create your views here.
@api_view(["POST"])
def signup(request):
    """Function to add new user"""
    try:
        data = request.data
        serializer = UserSignUpSerializer(data=data)
        if serializer.is_valid():
            first_name = serializer.data["first_name"]
            last_name = serializer.data["last_name"]
            password = serializer.data["password"]
            mobile_number = serializer.data['mobile_number']
            age = serializer.data['age']
            designation_title = serializer.data['designation_title']
            designation = serializer.data['designation']
            is_medicine_ongoing = serializer.data['is_medicine_ongoing']
            any_health_issues = serializer.data['any_health_issues']
            profile_pic = request.FILES['profile_pic']
            user = UserModel.objects.filter(
                first_name=first_name,last_name=last_name,password=password,mobile_number=mobile_number).first()
            if user:
                return Response(
                    ResponseData.error(
                        "User is already registered please log in"),
                    status=status.HTTP_201_CREATED,
                )
            if profile_pic!="":
                 fs = FileSystemStorage(location='static/')
                 fs.save(profile_pic.name, profile_pic)
            new_user = UserModel.objects.create(
                first_name=first_name,
                last_name=last_name,
                mobile_number=mobile_number,
                profile_pic= "" if profile_pic == "" else f"static/{profile_pic}",
                password=password,
                age=age,
                designation_title=designation_title,
                designation=DesignationModel(id=designation),
                is_medicine_ongoing=is_medicine_ongoing,
                any_health_issues=any_health_issues
            )
            new_user.save()
            user_details = list(
                UserModel.objects.values().filter(id=new_user.id))
            return Response(
                ResponseData.success(
                    user_details[0]['id'], "User added successfully"),
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
def signin(request):
    """Function to let user sign in"""
    try:
        data = request.data
        serializer = UserSignInSerializer(data=data)
        print(f"IsValid: {serializer.is_valid()}")
        if serializer.is_valid():
            password = serializer.data["password"]
            username = serializer.data["username"]
            user = UserModel.objects.filter(
                first_name=str(username).split(".")[0],last_name=str(username).split(".")[1],password=password).first()
            if not user:
                return Response(
                    ResponseData.error(
                        "Account does not exists, please register first"),
                    status=status.HTTP_201_CREATED,
                )
            user_details = list(
                UserModel.objects.values().filter(first_name=str(username).split(".")[0],last_name=str(username).split(".")[1],
                 password=password))
            return JsonResponse(
                    ResponseData.success(
                        user_details[0]['id'], "User logged in successfully"),
                    safe=False,
                )
        return Response(
            ResponseData.error(serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@api_view(["POST"])
def is_user_subscribed(request):
    """Function to let user sign in"""
    try:
        data = request.data
        serializer = UserSubscribedOrNotSerializer(data=data)
        print(f"IsValid: {serializer.is_valid()}")
        if serializer.is_valid():
            user_id = serializer.data['id']
            print(f'user_id {serializer.data}')
            user = UserModel.objects.filter(
                id=user_id).first()
            if not user:
                return Response(
                    ResponseData.error(
                        "Account does not exists, please register first"),
                    status=status.HTTP_201_CREATED,
                )
            return JsonResponse(
                    ResponseData.user_subscribed(
                        "Api called successfully", user.is_subscribed),
                    safe=False,
                )
        return Response(
            ResponseData.error(serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@api_view(["POST"])
def addNewPayment(request):
    """Function to add new payment done by a user"""
    try:
        data = request.data
        serializer = AddNewPaymentSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            payment_id = serializer.data["payment_id"]
            subscription_id = serializer.data["subscription"]
            date_of_payment = serializer.data['date_of_payment']
            new_payment_record = UserPaymentDetailsModel.objects.create(
                user_id=UserModel(id=user_id),
                payment_id=payment_id,
                subscription=SubscriptionModel(id=subscription_id),
                date_of_payment=date_of_payment,
            )
            new_payment_record.save()
            # payment_details = list(
            #     UserPaymentDetailsModel.objects.values().filter(id=new_payment_record.id))
            user_data = UserModel.objects.filter(
                    id=user_id
                ).first()
            user_data.is_subscribed = True
            user_data.save()
            return Response(
                ResponseData.success_without_data(
                    "Payment done successfully"),
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
def addNewSubscription(request):
    """Function to add new subscription details of a user"""
    try:
        data = request.data
        serializer = AddUserSubscriptionSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user"]
            subscription_id = serializer.data["subscription"]
            user = UserModel.objects.filter(
                id=user_id).first()
            if not user:
                return Response(
                    ResponseData.error(
                        "User id is invalid"),
                    status=status.HTTP_201_CREATED,
                )
            subscription = SubscriptionModel.objects.filter(
                id=subscription_id).first()
            if not subscription:
                return Response(
                    ResponseData.error(
                        "Subscription id is invalid"),
                    status=status.HTTP_201_CREATED,
                )
            new_subscription = UserSubscriptionDetailsModel.objects.create(
                user=UserModel(id=user_id),
                subscription=SubscriptionModel(id=subscription_id)
            )
            new_subscription.save()
            return Response(
                ResponseData.success_without_data(
                    "Subscription done successfully"),
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
def getUserSubscriptionById(request):
    """Function to get subscription based on user id"""
    try:
        data = request.data
        serializer = GetUserSubscriptionSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user"]
            subscription_id = serializer.data["subscription"]
            user = UserModel.objects.filter(
                id=user_id).first()
            if not user:
                return Response(
                    ResponseData.error(
                        "User id is invalid"),
                    status=status.HTTP_201_CREATED,
                )
            subscription = SubscriptionModel.objects.filter(
                id=subscription_id).first()
            if not subscription:
                return Response(
                    ResponseData.error(
                        "Subscription id is invalid"),
                    status=status.HTTP_201_CREATED,
                )
            subscription_data = UserSubscriptionDetailsModel.objects.values().filter(id=subscription_id,user=UserModel(id=user_id)).all()
            for i in range(0,len(subscription_data)):
                subscription_data[i].pop('created_at')
                subscription_data[i].pop('updated_at')
            return Response(
                ResponseData.success(
                    subscription_data, "Subscription fetched successfully"),
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

@api_view(["POST"])
def getAllSubscriptionsOfUser(request):
    """Function to get all subscriptions of a user"""
    try:
        data = request.data
        serializer = GetUserSubscriptionSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user"]
            user = UserModel.objects.filter(
                id=user_id).first()
            if not user:
                return Response(
                    ResponseData.error(
                        "User id is invalid"),
                    status=status.HTTP_201_CREATED,
                )
            subscription_data = UserSubscriptionDetailsModel.objects.values().filter(user=UserModel(id=user_id)).all()
            for i in range(0,len(subscription_data)):
                subscription_data[i].pop('created_at')
                subscription_data[i].pop('updated_at')
            return Response(
                ResponseData.success(
                    subscription_data, "Subscriptions fetched successfully"),
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


@api_view(["POST"])
def getAllUsersDetails(request):
    """Function to get details of all users"""
    try:
        request_data = request.data
        page_number = int(request_data['page_no'])
        page_size_param = int(request_data['page_size'])
        search_param = request_data['search_param'] if 'search_param' in request.data else ""
        page_no = page_number
        page_size = page_size_param
        start=(page_no-1)*page_size
        end=page_no*page_size
        print(start)
        print(end)
        print(f"request_data {request_data}")
        if(request_data['filterByCategory'] == "" and request_data['filterByDesignation'] == "" and request_data['sortBy'] == "" and search_param == ""):
           users_data = UserModel.objects.values().filter().order_by('-joining_date').all()
        #    users_data = UserModel.objects.values().filter().order_by('-joining_date').all()[start:end]
        elif(request_data['sortBy'] == "Age (max to min)" and request_data['filterByDesignation'] == ""):
           users_data = UserModel.objects.values().filter().order_by('-age').all()[start:end]
        elif(request_data['sortBy'] == "Age (min to max)" and request_data['filterByDesignation'] == ""):
           users_data = UserModel.objects.values().filter().order_by('age').all()[start:end]
        elif(request_data['sortBy'] == "Age (max to min)" and request_data['filterByDesignation'] != ""):
           users_data = UserModel.objects.values().filter(designation = DesignationModel(id=request_data['filterByDesignation'])).order_by('-age').all()[start:end]
        elif(request_data['sortBy'] == "Age (min to max)" and request_data['filterByDesignation'] != ""):
           users_data = UserModel.objects.values().filter(designation = DesignationModel(id=request_data['filterByDesignation'])).order_by('age').all()[start:end]
        elif(request_data['filterByDesignation'] != ""):
           print(f"ccsd {request_data['filterByDesignation']}")
           users_data = UserModel.objects.values().filter(designation = DesignationModel(id=request_data['filterByDesignation'])).all()[start:end]
        else:
           users_data = UserModel.objects.values().filter().all()
        if(request_data['filterByCategory']) != "" : 
            total_categories = CommitmentCategoryModel.objects.values().filter(name=request_data['filterByCategory']).all()
        else:
            total_categories = CommitmentCategoryModel.objects.values().filter().all()
        print(f"users_data length {len(users_data)}")
        if search_param != "":
           new_user_data = []
           for i in range(0,len(users_data)):
               if(str(users_data[i]['first_name']).lower().__contains__(str(search_param).lower()) or str(users_data[i]['last_name']).lower().__contains__(str(search_param).lower())
               or str(users_data[i]['mobile_number']).__contains__(search_param) or str(users_data[i]['age']).__contains__(search_param)):
                 new_user_data.append(users_data[i])
           users_data = new_user_data[start:end]
        print(f"users_data length after search {len(users_data)}")
        for i in range(0,len(users_data)):
            if(len(total_categories) > 1):     
                 commitments_data = CommitmentModel.objects.values().filter(user = UserModel(id=users_data[i]['id'])).all()
                 done_commitments_data = CommitmentModel.objects.values().filter(user = UserModel(id=users_data[i]['id']),is_done = True,is_updated = True).all()
                 notDone_commitments_data = CommitmentModel.objects.values().filter(user = UserModel(id=users_data[i]['id']),is_done = False,is_updated = True).all()
                 notUpdated_commitments_data = CommitmentModel.objects.values().filter(user = UserModel(id=users_data[i]['id']),is_done = False,is_updated = False).all()
                 users_data[i]['commitments_details'] = {}
                 users_data[i]['commitments_details']['total_commitments'] = len(commitments_data)
                 users_data[i]['commitments_details']['total_commitments_done'] = len(done_commitments_data)
                 users_data[i]['commitments_details']['total_commitments_not_done'] = len(notDone_commitments_data)
                 users_data[i]['commitments_details']['total_commitments_not_updated'] = len(notUpdated_commitments_data)
                 users_data[i]['commitments_details']['category_wise'] = []
            for j in range(0,len(total_categories)):
                data = {}
                commitments_data = CommitmentModel.objects.values().filter(user = UserModel(id=users_data[i]['id']),category = CommitmentCategoryModel(id=total_categories[j]['id'])).all()
                done_commitments_data = CommitmentModel.objects.values().filter(user = UserModel(id=users_data[i]['id']),category = CommitmentCategoryModel(id=total_categories[j]['id']),is_done = True,is_updated = True).all()
                notDone_commitments_data = CommitmentModel.objects.values().filter(user = UserModel(id=users_data[i]['id']),category = CommitmentCategoryModel(id=total_categories[j]['id']),is_done = False,is_updated = True).all()
                notUpdated_commitments_data = CommitmentModel.objects.values().filter(user = UserModel(id=users_data[i]['id']),category = CommitmentCategoryModel(id=total_categories[j]['id']),is_done = False,is_updated = False).all()
                if(len(total_categories) == 1):
                    users_data[i]['commitments_details'] = {}
                    users_data[i]['commitments_details']['total_commitments'] = len(commitments_data)
                    users_data[i]['commitments_details']['total_commitments_done'] = len(done_commitments_data)
                    users_data[i]['commitments_details']['total_commitments_not_done'] = len(notDone_commitments_data)
                    users_data[i]['commitments_details']['total_commitments_not_updated'] = len(notUpdated_commitments_data)
                    users_data[i]['commitments_details']['category_wise'] = []
                data['category_name'] = total_categories[j]['name']
                data['total_commitments'] = len(commitments_data)
                data['total_commitments_done'] = len(done_commitments_data)
                data['total_commitments_not_done'] = len(notDone_commitments_data)
                data['total_commitments_not_updated'] = len(notUpdated_commitments_data)
                users_data[i]['commitments_details']['category_wise'].append(data)
            users_data[i].pop('created_at')
            users_data[i].pop('updated_at')
            # users_data[i].pop('designation_id')
        print(f"dfvfd {request_data['sortBy']}")
        if(request_data['sortBy'] == 'Commitment done (min to max)'):
            users_data = sorted(users_data, key=lambda d: d['commitments_details']['total_commitments_done'])[start:end]
        elif(request_data['sortBy'] == 'Commitment done (max to min)'):
            users_data = sorted(users_data, key=lambda d: d['commitments_details']['total_commitments_done'],reverse=True)[start:end]
        final_data = []
        for i in range(0,len(users_data)):
            print(f"ddcdcd {users_data[i]['commitments_details']['total_commitments']}")
            if(users_data[i]['commitments_details']['total_commitments']!=0):
                final_data.append(users_data[i])
        print(f"final_data length {len(final_data)}")
        if(len(final_data) == 0):
          return Response(
            ResponseData.success(
                final_data, "No Data Found"),
            status=status.HTTP_201_CREATED)
        return Response(
            ResponseData.success(
                final_data, "User Details fetched successfully"),
            status=status.HTTP_201_CREATED)

    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["POST"])
def getOverallPerformerOfTheWeek(request):
    """Function to get overall performer of the week"""
    try:
        users_data = UserModel.objects.values().filter().all()
        today = datetime.now()
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        sub_start_date = datetime.strptime(str(start).split(" ")[0], "%Y-%m-%d").date()
        sub_end_date = datetime.strptime(str(end).split(" ")[0], "%Y-%m-%d").date()
        final_data = []
        for i in range(0,len(users_data)):
            max_done_commitments = {
            "user_id" : "",
            "max_commitments" : 0
        }
            users_data[i]['commitments'] = []
            max_done_commitments['user_id'] = users_data[i]['id']
            commitment_data = CommitmentModel.objects.values().filter(user = UserModel(id=users_data[i]['id']),is_done = True,is_updated = True).all()
            value = 0
            for j in range(0,len(commitment_data)):
                current_date = datetime.strptime(str(commitment_data[j]['commitment_date']).split(" ")[0], "%Y-%m-%d").date()
                if current_date >= sub_start_date and current_date <= sub_end_date:
                    value+=1
                    users_data[i]['commitments'].append(commitment_data[j])
            max_done_commitments['max_commitments'] = value
            final_data.append(max_done_commitments)
        newlist = sorted(final_data, key=lambda d: d['max_commitments'],reverse=True)
        tempList = []
        for i in range(0,len(newlist)):
            if(newlist[i]['max_commitments'] > 0):
                tempList.append(newlist[i])
        newlist = tempList
        user_ids = []
        print(f"newlist dcs {newlist}")
        if(len(newlist) == 0):
          return Response(
            ResponseData.success(
                [], "No user found"),
            status=status.HTTP_201_CREATED)
        user_ids.append(newlist[0]['user_id'])
        for j in range(1,len(newlist)):
                if(str(newlist[j]['max_commitments']) == str(newlist[0]['max_commitments'])):
                    user_ids.append(newlist[j]['user_id'])
        if(len(user_ids) == 0):
          return Response(
            ResponseData.success(
                [], "No Data Found"),
            status=status.HTTP_201_CREATED)
        total_categories = CommitmentCategoryModel.objects.values().filter().all()
        finalData = []
        for k in range(0,len(user_ids)):
            users_data = UserModel.objects.values().filter(id=user_ids[k]).all()
            for i in range(0,len(users_data)):
                commitments_data = CommitmentModel.objects.values().filter(user = UserModel(id=users_data[i]['id'])).all()
                temp_list = []
                users_data[i]['commitments_details'] = {}
                for j in range(0,len(commitments_data)):
                   current_date = datetime.strptime(str(commitments_data[j]['commitment_date']).split(" ")[0], "%Y-%m-%d").date()
                   if current_date >= sub_start_date and current_date <= sub_end_date:
                       temp_list.append(commitments_data[j])
                users_data[i]['commitments_details']['total_commitments'] = len(temp_list)
                done_commitments_data = CommitmentModel.objects.values().filter(user = UserModel(id=users_data[i]['id']),is_done = True,is_updated = True).all()
                temp_list = []
                for j in range(0,len(done_commitments_data)):
                   current_date = datetime.strptime(str(done_commitments_data[j]['commitment_date']).split(" ")[0], "%Y-%m-%d").date()
                   if current_date >= sub_start_date and current_date <= sub_end_date:
                       temp_list.append(done_commitments_data[j])
                users_data[i]['commitments_details']['total_commitments_done'] = len(temp_list)
                notDone_commitments_data = CommitmentModel.objects.values().filter(user = UserModel(id=users_data[i]['id']),is_done = False,is_updated = True).all()
                temp_list = []
                for j in range(0,len(notDone_commitments_data)):
                   current_date = datetime.strptime(str(notDone_commitments_data[j]['commitment_date']).split(" ")[0], "%Y-%m-%d").date()
                   if current_date >= sub_start_date and current_date <= sub_end_date:
                       temp_list.append(notDone_commitments_data[j])
                users_data[i]['commitments_details']['total_commitments_not_done'] = len(temp_list)
                notUpdated_commitments_data = CommitmentModel.objects.values().filter(user = UserModel(id=users_data[i]['id']),is_done = False,is_updated = False).all()
                temp_list = []
                for j in range(0,len(notUpdated_commitments_data)):
                   current_date = datetime.strptime(str(notUpdated_commitments_data[j]['commitment_date']).split(" ")[0], "%Y-%m-%d").date()
                   if current_date >= sub_start_date and current_date <= sub_end_date:
                       temp_list.append(notUpdated_commitments_data[j])
                users_data[i]['commitments_details']['total_commitments_not_updated'] = len(temp_list)
                temp_list = []
                users_data[i]['commitments_details']['category_wise'] = []
                for j in range(0,len(total_categories)):
                    data = {}
                    commitments_data = CommitmentModel.objects.values().filter(user = UserModel(id=users_data[i]['id']),category = CommitmentCategoryModel(id=total_categories[j]['id'])).all()
                    for k in range(0,len(commitments_data)):
                       current_date = datetime.strptime(str(commitments_data[k]['commitment_date']).split(" ")[0], "%Y-%m-%d").date()
                       if current_date >= sub_start_date and current_date <= sub_end_date:
                           temp_list.append(commitments_data[k])
                    data['total_commitments'] = len(temp_list)
                    temp_list = []
                    done_commitments_data = CommitmentModel.objects.values().filter(user = UserModel(id=users_data[i]['id']),category = CommitmentCategoryModel(id=total_categories[j]['id']),is_done = True,is_updated = True).all()
                    for k in range(0,len(done_commitments_data)):
                       current_date = datetime.strptime(str(done_commitments_data[k]['commitment_date']).split(" ")[0], "%Y-%m-%d").date()
                       if current_date >= sub_start_date and current_date <= sub_end_date:
                           temp_list.append(done_commitments_data[k])
                    data['total_commitments_done'] = len(temp_list)
                    temp_list = []
                    notDone_commitments_data = CommitmentModel.objects.values().filter(user = UserModel(id=users_data[i]['id']),category = CommitmentCategoryModel(id=total_categories[j]['id']),is_done = False,is_updated = True).all()
                    for k in range(0,len(notDone_commitments_data)):
                       current_date = datetime.strptime(str(notDone_commitments_data[k]['commitment_date']).split(" ")[0], "%Y-%m-%d").date()
                       if current_date >= sub_start_date and current_date <= sub_end_date:
                           temp_list.append(notDone_commitments_data[k])
                    data['total_commitments_not_done'] = len(temp_list)
                    temp_list = []
                    notUpdated_commitments_data = CommitmentModel.objects.values().filter(user = UserModel(id=users_data[i]['id']),category = CommitmentCategoryModel(id=total_categories[j]['id']),is_done = False,is_updated = False).all()
                    for k in range(0,len(notUpdated_commitments_data)):
                       current_date = datetime.strptime(str(notUpdated_commitments_data[k]['commitment_date']).split(" ")[0], "%Y-%m-%d").date()
                       if current_date >= sub_start_date and current_date <= sub_end_date:
                           temp_list.append(notUpdated_commitments_data[k])
                    data['total_commitments_not_updated'] = len(temp_list)
                    temp_list = []
                    data['category_name'] = total_categories[j]['name']
                    users_data[i]['commitments_details']['category_wise'].append(data)
                users_data[i].pop('created_at')
                users_data[i].pop('updated_at')
            finalData.append(users_data[i])
        return Response(
            ResponseData.success(
                finalData, "User Details fetched successfully"),
            status=status.HTTP_201_CREATED)

    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["POST"])
def getOverallPerformerOfTheWeekCategoryWise(request):
    """Function to get overall performer of the week"""
    try:
        all_users_data = UserModel.objects.values().filter().all()
        today = datetime.now()
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        sub_start_date = datetime.strptime(str(start).split(" ")[0], "%Y-%m-%d").date()
        sub_end_date = datetime.strptime(str(end).split(" ")[0], "%Y-%m-%d").date()
        total_categories = CommitmentCategoryModel.objects.values().filter().all()
        final_next_data = []
        for index in range(0,len(total_categories)):
            final_data = []
            for i in range(0,len(all_users_data)):
                max_done_commitments = {
                "user_id" : "",
                "max_commitments" : 0
                }
                all_users_data[i]['commitments'] = []
                max_done_commitments['user_id'] = all_users_data[i]['id']
                commitment_data = CommitmentModel.objects.values().filter(user = UserModel(id=all_users_data[i]['id']),is_done = True,is_updated = True,category = CommitmentCategoryModel(id=total_categories[index]['id'])).all()
                value = 0
                for j in range(0,len(commitment_data)):
                    current_date = datetime.strptime(str(commitment_data[j]['commitment_date']).split(" ")[0], "%Y-%m-%d").date()
                    if current_date >= sub_start_date and current_date <= sub_end_date:
                        value+=1
                        all_users_data[i]['commitments'].append(commitment_data[j])
                max_done_commitments['max_commitments'] = value
                final_data.append(max_done_commitments)
            newlist = sorted(final_data, key=lambda d: d['max_commitments'],reverse=True)
            tempList = []
            for i in range(0,len(newlist)):
                if(newlist[i]['max_commitments'] > 0):
                    tempList.append(newlist[i])
            newlist = tempList
            user_ids = []
            print(f"newlist dcs {newlist}")
            if(len(newlist) == 0):
              return Response(
                ResponseData.success(
                    [], "No user found"),
                status=status.HTTP_201_CREATED)
            user_ids = []
            user_ids.append(newlist[0]['user_id'])
            for j in range(1,len(newlist)):
                    if(str(newlist[j]['max_commitments']) == str(newlist[0]['max_commitments'])):
                        user_ids.append(newlist[j]['user_id'])
            if(len(user_ids) == 0):
              return Response(
                ResponseData.success(
                    [], "No Data Found"),
                status=status.HTTP_201_CREATED)
            finalData = []
            for k in range(0,len(user_ids)):
                users_data = UserModel.objects.values().filter(id=user_ids[k]).all()
                for i in range(0,len(users_data)):
                    commitments_data = CommitmentModel.objects.values().filter(user = UserModel(id=users_data[i]['id'])).all()
                    temp_list = []
                    users_data[i]['commitments_details'] = {}
                    for j in range(0,len(commitments_data)):
                       current_date = datetime.strptime(str(commitments_data[j]['commitment_date']).split(" ")[0], "%Y-%m-%d").date()
                       if current_date >= sub_start_date and current_date <= sub_end_date:
                           temp_list.append(commitments_data[j])
                    users_data[i]['commitments_details']['total_commitments'] = len(temp_list)
                    done_commitments_data = CommitmentModel.objects.values().filter(user = UserModel(id=users_data[i]['id']),is_done = True,is_updated = True).all()
                    temp_list = []
                    for j in range(0,len(done_commitments_data)):
                       current_date = datetime.strptime(str(done_commitments_data[j]['commitment_date']).split(" ")[0], "%Y-%m-%d").date()
                       if current_date >= sub_start_date and current_date <= sub_end_date:
                           temp_list.append(done_commitments_data[j])
                    users_data[i]['commitments_details']['total_commitments_done'] = len(temp_list)
                    notDone_commitments_data = CommitmentModel.objects.values().filter(user = UserModel(id=users_data[i]['id']),is_done = False,is_updated = True).all()
                    temp_list = []
                    for j in range(0,len(notDone_commitments_data)):
                       current_date = datetime.strptime(str(notDone_commitments_data[j]['commitment_date']).split(" ")[0], "%Y-%m-%d").date()
                       if current_date >= sub_start_date and current_date <= sub_end_date:
                           temp_list.append(notDone_commitments_data[j])
                    users_data[i]['commitments_details']['total_commitments_not_done'] = len(temp_list)
                    notUpdated_commitments_data = CommitmentModel.objects.values().filter(user = UserModel(id=users_data[i]['id']),is_done = False,is_updated = False).all()
                    temp_list = []
                    for j in range(0,len(notUpdated_commitments_data)):
                       current_date = datetime.strptime(str(notUpdated_commitments_data[j]['commitment_date']).split(" ")[0], "%Y-%m-%d").date()
                       if current_date >= sub_start_date and current_date <= sub_end_date:
                           temp_list.append(notUpdated_commitments_data[j])
                    users_data[i]['commitments_details']['total_commitments_not_updated'] = len(temp_list)
                    temp_list = []
                    users_data[i]['commitments_details']['category_wise'] = []
                    for j in range(0,len(total_categories)):
                        data = {}
                        commitments_data = CommitmentModel.objects.values().filter(user = UserModel(id=users_data[i]['id']),category = CommitmentCategoryModel(id=total_categories[j]['id'])).all()
                        for k in range(0,len(commitments_data)):
                           current_date = datetime.strptime(str(commitments_data[k]['commitment_date']).split(" ")[0], "%Y-%m-%d").date()
                           if current_date >= sub_start_date and current_date <= sub_end_date:
                               temp_list.append(commitments_data[k])
                        data['total_commitments'] = len(temp_list)
                        temp_list = []
                        done_commitments_data = CommitmentModel.objects.values().filter(user = UserModel(id=users_data[i]['id']),category = CommitmentCategoryModel(id=total_categories[j]['id']),is_done = True,is_updated = True).all()
                        for k in range(0,len(done_commitments_data)):
                           current_date = datetime.strptime(str(done_commitments_data[k]['commitment_date']).split(" ")[0], "%Y-%m-%d").date()
                           if current_date >= sub_start_date and current_date <= sub_end_date:
                               temp_list.append(done_commitments_data[k])
                        data['total_commitments_done'] = len(temp_list)
                        temp_list = []
                        notDone_commitments_data = CommitmentModel.objects.values().filter(user = UserModel(id=users_data[i]['id']),category = CommitmentCategoryModel(id=total_categories[j]['id']),is_done = False,is_updated = True).all()
                        for k in range(0,len(notDone_commitments_data)):
                           current_date = datetime.strptime(str(notDone_commitments_data[k]['commitment_date']).split(" ")[0], "%Y-%m-%d").date()
                           if current_date >= sub_start_date and current_date <= sub_end_date:
                               temp_list.append(notDone_commitments_data[k])
                        data['total_commitments_not_done'] = len(temp_list)
                        temp_list = []
                        notUpdated_commitments_data = CommitmentModel.objects.values().filter(user = UserModel(id=users_data[i]['id']),category = CommitmentCategoryModel(id=total_categories[j]['id']),is_done = False,is_updated = False).all()
                        for k in range(0,len(notUpdated_commitments_data)):
                           current_date = datetime.strptime(str(notUpdated_commitments_data[k]['commitment_date']).split(" ")[0], "%Y-%m-%d").date()
                           if current_date >= sub_start_date and current_date <= sub_end_date:
                               temp_list.append(notUpdated_commitments_data[k])
                        data['total_commitments_not_updated'] = len(temp_list)
                        temp_list = []
                        data['category_name'] = total_categories[j]['name']
                        users_data[i]['commitments_details']['category_wise'].append(data)
                        users_data[i]['category_name'] = total_categories[index]['name']
                users_data[i].pop('created_at')
                users_data[i].pop('updated_at')
                finalData.append(users_data[i])
            for i in range(0,len(finalData)):
               final_next_data.append(finalData[i])
        return Response(
            ResponseData.success(
                final_next_data, "User Details fetched successfully"),
            status=status.HTTP_201_CREATED)

    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["POST"])
def updateProfile(request):
    """Function to update user profile"""
    try:
        data = request.data
        serializer = UserSignUpSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["id"]
            first_name = serializer.data["first_name"]
            last_name = serializer.data["last_name"]
            mobile_number = serializer.data["mobile_number"]
            password = serializer.data["password"]
            age = serializer.data["age"]
            designation_title = serializer.data["designation_title"]
            designation = serializer.data["designation"]
            is_medicine_ongoing = serializer.data["is_medicine_ongoing"]
            any_health_issues = serializer.data["any_health_issues"]
            is_subscribed = serializer.data["is_subscribed"]
            userdata = UserModel.objects.filter(
                id=user_id
            ).first()
            if not userdata:
                return Response(
                    ResponseData.error("User id is invalid."),
                    status=status.HTTP_200_OK,
                )
            if 'profile_pic' in request.FILES:
                fs = FileSystemStorage(location='static/')
                fs.save(request.FILES['profile_pic'].name, request.FILES['profile_pic'])
            if 'profile_pic' in request.FILES:
               userdata.first_name=first_name
               userdata.profile_pic = f"static/{request.FILES['profile_pic']}"
               userdata.last_name=last_name
               userdata.mobile_number = mobile_number
               userdata.password = password
               userdata.age = age
               userdata.designation_title = designation_title
               userdata.designation = DesignationModel(id=designation)
               userdata.is_medicine_ongoing = is_medicine_ongoing
               userdata.any_health_issues = any_health_issues
               userdata.is_subscribed = is_subscribed
               userdata.save()
               print("true")
            else:
               userdata.first_name=first_name
            #    userdata.profile_pic = f"static/{request.FILES['profile_pic']}"
               userdata.last_name=last_name
               userdata.mobile_number = mobile_number
               userdata.password = password
               userdata.age = age
               userdata.designation_title = designation_title
               userdata.designation = DesignationModel(id=designation)
               userdata.is_medicine_ongoing = is_medicine_ongoing
               userdata.any_health_issues = any_health_issues
               userdata.is_subscribed = is_subscribed
               userdata.save()
               print("true")
            updated_date = list(
                UserModel.objects.values().filter(
                    id=user_id)
            )
            return Response(
                ResponseData.success(
                    updated_date[0]['id'], "User profile updated successfully"),
                status=status.HTTP_201_CREATED,
            )
        print("serializer.errors")
        print(serializer.errors)
        return Response(
            ResponseData.error(serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )
    except KeyError as exception:
        print("exception")
        print(exception)
        return Response(
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@api_view(["POST"])
def getUserProfileDetails(request):
    """Function to get user profile details based on user id"""
    try:
        data = request.data
        serializer = GetUserProfileSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["id"]
            user = UserModel.objects.filter(
                id=user_id).first()
            if not user:
                return Response(
                    ResponseData.error(
                        "User id is invalid"),
                    status=status.HTTP_201_CREATED,
                )
            user_details = UserModel.objects.values().filter(id=user_id).all()
            user_details[0].pop('created_at')
            user_details[0].pop('updated_at')
            return Response(
                ResponseData.success(
                    user_details, " User details fetched successfully"),
                status=status.HTTP_201_CREATED)
        return Response(
                    ResponseData.error(serializer.errors),
                    status=status.HTTP_400_BAD_REQUEST,
                )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )