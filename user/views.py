from django.shortcuts import render
from rest_framework.decorators import api_view
from user.models import UserModel
from rest_framework.response import Response
from user.serializers import UserSignInSerializer, UserSignUpSerializer
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
            mobile_number = serializer.data["mobile_number"]
            user = UserModel.objects.filter(
                mobile_number=mobile_number, password=password).first()
            if not user:
                return Response(
                    ResponseData.error(
                        "Account does not exists, please register first"),
                    status=status.HTTP_201_CREATED,
                )
            user_details = list(
                UserModel.objects.values().filter(mobile_number=mobile_number, password=password))
            return JsonResponse(
                    ResponseData.success(
                        user_details[0], "User logged in successfully"),
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