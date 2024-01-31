import os

import requests as R

# Create your views here.
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from commdem_warriors_backend.authenticators import ApiKeyAuthentication
from notifications.models import UserPlayerIdModel
from notifications.serializers import SendNotificationToUserSerializer
from redeemPoints.models import RedeemPointsModel
from referralCode.models import ReferralCodeModel
from response import Response as ResponseData
from user.models import (
    UserGoogleSignInModel,
    UserHealthDetailsModel,
    UserLocationDetailsModel,
    UserModel,
    UserProfessionalDetailsModel,
    UserSubscriptionDetailsModel,
)

load_dotenv()


@api_view(["POST"])
@authentication_classes(
    [
        ApiKeyAuthentication,
    ]
)
def send_notification_to_admin():
    """Function to send notification to admin when new user signs up"""
    try:
        list_of_player_ids = []
        all_admin_users = UserModel.objects.filter(is_admin=True, is_active=True).all()
        for i in range(0, all_admin_users.count()):
            admin_player_id = UserPlayerIdModel.objects.filter(
                user_id=all_admin_users[i].id, is_active=True
            ).get()
            list_of_player_ids.append(admin_player_id.player_id)
        print(list_of_player_ids)
        data = {
            "app_id": os.getenv("ONESIGNAL_APP_ID"),
            "include_player_ids": list_of_player_ids,
            "data": {"foo": "New user joined recently"},
            "contents": {"en": "Please check if profile is valid or not"},
        }
        R.post(f"{os.getenv('BASE_URL')}/notifications", json=data)
        return Response(
            ResponseData.success_without_data(
                "Notification has been sent to admin for verification"
            ),
            status=status.HTTP_201_CREATED,
        )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@authentication_classes(
    [
        ApiKeyAuthentication,
    ]
)
def send_verification_notification_to_user(request):
    """Function to send notification to user whose verification is done by admin"""
    try:
        data = request.data
        serializer = SendNotificationToUserSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            isVerified = serializer.data["isVerified"]
            userDetails = UserModel.objects.filter(id=user_id).get()
            list_of_player_ids = []
            user_player_id = UserPlayerIdModel.objects.filter(user_id=user_id).all()
            for j in range(0, user_player_id.count()):
                list_of_player_ids.append(user_player_id[j].player_id)
            print(list_of_player_ids)
            if isVerified:
                userDetails.is_active = True
                userSubscriptionDetails = UserSubscriptionDetailsModel.objects.filter(
                    user_id=user_id
                ).first()
                if userSubscriptionDetails is not None:
                    userSubscriptionDetails.is_active = True
                    userSubscriptionDetails.save()
                userGoogleAccountDetails = UserGoogleSignInModel.objects.filter(
                    user_id=user_id
                ).first()
                if userGoogleAccountDetails is not None:
                    userGoogleAccountDetails.is_active = True
                    userGoogleAccountDetails.save()
                userLocationDetails = UserLocationDetailsModel.objects.filter(
                    user_id=user_id
                ).first()
                if userLocationDetails is not None:
                    userLocationDetails.is_active = True
                    userLocationDetails.save()
                userProfessionalDetails = UserProfessionalDetailsModel.objects.filter(
                    user_id=user_id
                ).first()
                if userProfessionalDetails is not None:
                    userProfessionalDetails.is_active = True
                    userProfessionalDetails.save()
                userHealthDetails = UserHealthDetailsModel.objects.filter(
                    user_id=user_id
                ).first()
                if userHealthDetails is not None:
                    userHealthDetails.is_active = True
                    userHealthDetails.save()
                userReferralCodeDetails = ReferralCodeModel.objects.filter(
                    user_id=user_id
                ).first()
                if userReferralCodeDetails is not None:
                    userReferralCodeDetails.is_active = True
                    userReferralCodeDetails.save()
                userRedeemPointsDetails = RedeemPointsModel.objects.filter(
                    from_user_id=user_id
                ).first()
                if userRedeemPointsDetails is not None:
                    userRedeemPointsDetails.is_active = True
                    userRedeemPointsDetails.save()
                userDetails.is_verified = isVerified
                userDetails.save()
                data = {
                    "app_id": os.getenv("ONESIGNAL_APP_ID"),
                    "include_player_ids": list_of_player_ids,
                    "data": {"foo": "Verification successfull"},
                    "contents": {
                        "en": "Now you can login into the application with your registered mobile number"
                    },
                }
                R.post(f"{os.getenv('BASE_URL')}/notifications", json=data)
                return Response(
                    ResponseData.success([], "Notification has been sent to the user"),
                    status=status.HTTP_201_CREATED,
                )
            else:
                userDetails.is_active = False
                data = {
                    "app_id": os.getenv("ONESIGNAL_APP_ID"),
                    "include_player_ids": list_of_player_ids,
                    "data": {"foo": "Verification declined"},
                    "contents": {"en": "We could not verify your details."},
                }
                R.post(f"{os.getenv('BASE_URL')}/notifications", json=data)
                return Response(
                    ResponseData.success([], "Notification has been sent to the user"),
                    status=status.HTTP_201_CREATED,
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
