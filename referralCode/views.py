from rest_framework.decorators import api_view
from rest_framework.response import Response
from location.models import CitiesModel
from designation.models import DesignationModel
from income.models import IncomeModel
from redeemPoints.models import RedeemPointsModel
from referralCode.models import ReferralCodeModel
from referralCode.serializers import GetReferralCodeSerializer
from response import Response as ResponseData
from rest_framework import status
from django.core.cache import cache
from subscription.models import SubscriptionModel

from subscription.serializers import GetSubscriptionSerializer
from user.models import UserHealthDetailsModel, UserLocationDetailsModel, UserModel, UserPaymentDetailsModel, UserProfessionalDetailsModel

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
            data = ReferralCodeModel.objects.values().filter().all()
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
def get_all_referrals_of_user(request):
    """Function to get all referral users of given user"""
    try:
        data = request.data
        serializer = GetReferralCodeSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            is_id_valid = UserModel.objects.filter(id=user_id).first()
            if not is_id_valid:
                   return Response(
                       ResponseData.error("User id is invalid"),
                       status=status.HTTP_200_OK,
                   )
            data = RedeemPointsModel.objects.values().filter(to_user_id=user_id).all()
            user_data = []
            for i in range(0,len(data)):
               mapData = {}
               user = UserModel.objects.values().filter(id=data[i]['from_user_id']).get()
               mapData['user_id'] = user['id']
               mapData['full_name'] = user['full_name']
               mapData['profile_pic'] = user['profile_pic']
               mapData['date_of_joining'] = str(user['joining_date']).split(' ')[0]
               city = UserLocationDetailsModel.objects.values().filter(user_id=data[i]['from_user_id']).first()
               if city is not None:
                  mapData['city_name'] = CitiesModel.objects.values().filter(id=city['city_id']).get()['name']
               income_range_id = UserProfessionalDetailsModel.objects.values().filter(user=UserModel(id=data[i]['from_user_id'])).first()
               if income_range_id is not None:
                  mapData['occupation'] = DesignationModel.objects.values().filter(id=income_range_id['designation_id']).get()['title']
                  mapData['designation_title'] = income_range_id['designation_title']
               mapData['age'] = UserHealthDetailsModel.objects.values().filter(user=UserModel(id=data[i]['from_user_id'])).get()['age']
               payment_details = list(UserPaymentDetailsModel.objects.values().filter(user_id=data[i]['from_user_id']))
               for j in range(0,len(payment_details)):
                   subscription_details = list(SubscriptionModel.objects.values().filter(
                        id=payment_details[j]['subscription_id']
                    ))
                   if(len(subscription_details) > 0):
                    subscription_details[0].pop('updated_at')
                    subscription_details[0].pop('created_at')
                    subscription_details[0]['level_name_id'] = 0
                    payment_details[j]['subscription_details'] = subscription_details[0]
                   else:
                    payment_details[j]['subscription_details'] = {}
                   payment_details[j].pop('updated_at')
                   payment_details[j].pop('created_at')
               mapData['subscriptions'] = payment_details
               user_data.append(mapData)
            return Response(
                   ResponseData.success(
                       user_data, "User referrals details fetched successfully"),
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
            is_id_valid = UserModel.objects.filter(id=user_id).first()
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