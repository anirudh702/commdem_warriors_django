from django.shortcuts import render
from rest_framework.decorators import api_view
from subscription.models import SubscriptionModel
from user.models import UserModel, UserPaymentDetailsModel, UserSubscriptionDetailsModel
from rest_framework.response import Response
from user.serializers import AddNewPaymentSerializer, AddUserSubscriptionSerializer, GetUserSubscriptionSerializer, UserSignInSerializer, UserSignUpSerializer, UserSubscribedOrNotSerializer
from django.core.files.storage import FileSystemStorage
from response import Response as ResponseData
from rest_framework import status
from django.http.response import JsonResponse

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
            designation = serializer.data['designation']
            is_medicine_ongoing = serializer.data['is_medicine_ongoing']
            any_health_issues = serializer.data['any_health_issues']
            profile_pic = request.FILES['profile_pic']
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
                designation=designation,
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