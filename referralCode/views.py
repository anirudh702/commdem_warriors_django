from rest_framework.decorators import api_view
from rest_framework.response import Response
from redeemPoints.models import RedeemPointsModel
from referralCode.models import ReferralCodeModel
from referralCode.serializers import GetReferralCodeSerializer
from response import Response as ResponseData
from rest_framework import status
from django.core.cache import cache
from subscription.models import SubscriptionModel

from subscription.serializers import GetSubscriptionSerializer
from user.models import UserModel

# Create your views here.

@api_view(["POST"])
def get_referral_code_of_user(request):
    """Function to get referral code details of a user"""
    try:
        data = request.data
        serializer = GetReferralCodeSerializer(data=data)
        if serializer.is_valid():
            # user_id = serializer.data["user_id"]
            # is_id_valid = UserModel.objects.filter(id=user_id).first()
            # if not is_id_valid:
            #        return Response(
            #            ResponseData.error("User id is invalid"),
            #            status=status.HTTP_200_OK,
            #        )
            data = ReferralCodeModel.objects.using('referralCode_db').values().filter().all()
            print(f"data {data}")
            for i in range(0,data.count()):
                data[i].pop('created_at')
                data[i].pop('updated_at')
            return Response(
                ResponseData.success(
                    data, "Referall code details fetched successfully"),
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
def delete_referral_code_of_user(request):
    """Function to delete referral code of a user"""
    try:
        data = request.data
        serializer = GetReferralCodeSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            is_id_valid = UserModel.objects.using('user_db').filter(id=user_id).first()
            # if not is_id_valid:
            #        return Response(
            #            ResponseData.error("User id is invalid"),
            #            status=status.HTTP_200_OK,
            #        )
            ReferralCodeModel.objects.filter().delete()
            return Response(
                ResponseData.success_without_data("Referral code delete successfully"),
                status=status.HTTP_201_CREATED)
        return Response(
                    ResponseData.error(serializer.errors),
                    status=status.HTTP_400_BAD_REQUEST,
                )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )