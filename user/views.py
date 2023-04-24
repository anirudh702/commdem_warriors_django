from rest_framework.decorators import api_view
from location.models import CitiesModel, CountriesDialCodeModel
from commitment.models import CommitmentCategoryModel, CommitmentModel, UserCommitmentsForNextWeekModel
from designation.models import DesignationModel
from income.models import IncomeModel
from location.models import CountriesModel, StatesModel
from notifications.models import UserPlayerIdModel
from notifications.views import send_notification_to_admin
from redeemPoints.models import RedeemPointsModel
from referralCode.models import ReferralCodeModel
from reviews.models import ReviewModel
from subscription.models import SubscriptionModel
from user.models import PaymentForReferralUsersModel, ReferralPaymentStatusModel, UserCashbackModel, UserGoogleSignInModel, UserHealthDetailsModel, UserLocationDetailsModel, UserModel, UserPaymentDetailsModel, UserPrivacyModel, UserProfessionalDetailsModel, UserReviewModel, UserSubscriptionDetailsModel, UserWisePrivacyModel
from rest_framework.response import Response
from user.serializers import AddNewPaymentSerializer, AddUserReviewSerializer, AddUserSubscriptionSerializer, GetReviewsOfAllUsersSerializer, GetUserProfileSerializer, GetUserSubscriptionSerializer, UpdateUserPrivacySerializer, UpdateUserReviewSerializer, UserSignInSerializer, UserSignUpSerializer, UserSubscribedOrNotSerializer
from django.core.files.storage import FileSystemStorage
from response import Response as ResponseData
from rest_framework import status
from django.http.response import JsonResponse
from datetime import *
from django.db.models import Q
from random import randint
import requests as R
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
import os
from django.db.models import Sum, F
from django.db.models.expressions import Window
from django.db.models.functions import Rank
from voiceAssistant.models import userPreferredVoiceLanguageModel, voiceAssistantLanguagesModel 
import razorpay
from django.utils.dateparse import parse_date

from voiceAssistant.views import addAllAfterUpdateVoicesLocally
load_dotenv()

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)



# Create your views here.
@api_view(["POST"])
def signup(request):
    """Function to add new user"""
    try:
        data = request.data
        serializer = UserSignUpSerializer(data=data)
        print(data)
        print(serializer.is_valid())
        if serializer.is_valid():
            full_name = serializer.data["full_name"]
            mobile_number = serializer.data['mobile_number']
            password = serializer.data["password"]
            email = serializer.data['email']
            virtual_assistant_language_id = serializer.data['virtual_assistant_language_id']
            birth_date = serializer.data['birth_date']
            profile_pic = request.FILES['profile_pic'] if'profile_pic' in request.FILES else ''
            referral_code = serializer.data['referral_code'] if 'referral_code' in data else 0
            gender = serializer.data['gender']
            weight = serializer.data['weight']
            height = serializer.data['height']
            age = serializer.data['age']
            designation_title = serializer.data['designation_title']
            designation = serializer.data['designation']
            city_id = serializer.data['city_id']
            state_id = serializer.data['state_id']
            country_id = serializer.data['country_id']
            # income_range = serializer.data['income_range']
            is_medicine_ongoing = serializer.data['is_medicine_ongoing']
            any_health_issues = serializer.data['any_health_issues']
            player_id = serializer.data['player_id'] if 'player_id' in request.data else ""
            user_uid = serializer.data['user_uid'] if 'user_uid' in request.data else ""
            user_gmail_id = serializer.data['user_gmail_id'] if 'user_gmail_id' in request.data else ""
            user = UserModel.objects.filter(
                Q(email__icontains=email) | Q(mobile_number__icontains=mobile_number)).first()
            if user:
                return Response(
                    ResponseData.error(
                        "User is already registered please log in"),
                    status=status.HTTP_201_CREATED,
                )
            if(referral_code!=0):
              referral_code_data = ReferralCodeModel.objects.filter(
                  referral_code=referral_code).get()
              if referral_code_data is None:
                  return Response(
                      ResponseData.error(
                          "Referral code is invalid"),
                      status=status.HTTP_201_CREATED,
                  )
            if profile_pic!="":
                 fs = FileSystemStorage(location='static/')
                 fs.save(profile_pic.name, profile_pic)
            new_user = UserModel.objects.create(
                full_name=full_name,
                mobile_number=mobile_number,
                email=email,
                profile_pic= "" if profile_pic == "" else f"static/{profile_pic}",
                password=password,
                birth_date=birth_date,
                referred_user_code=referral_code,
                is_verified = True if mobile_number == "+917020829599" else False,
                is_admin = True if mobile_number == "+917020829599" else False,
                is_active=True if mobile_number == "+917020829599" else False,
            )
            new_user.save()
            user_privacy_creation = UserPrivacyModel.objects.create(
                user_id=new_user.id,
            )
            user_privacy_creation.save()
            city_name = CitiesModel.objects.filter(id=city_id).first()
            new_user_location = UserLocationDetailsModel.objects.create(
                user_id=new_user.id,
                city_id=city_id,
                state_id=state_id,
                country_id=country_id, 
                city_name=city_name.name
            )
            new_user_location.save()
            new_user_professional_details = UserProfessionalDetailsModel.objects.create(
                designation_title=designation_title,
                user=UserModel(id=new_user.id),
                designation_id=designation,
                # income_range_id=income_range,
            )
            new_user_professional_details.save()
            new_user_health_details = UserHealthDetailsModel.objects.create(
                user=UserModel(id=new_user.id),
                weight=weight,
                height=height,
                gender=gender,
                age=age,
                is_medicine_ongoing=is_medicine_ongoing,
                any_health_issues=any_health_issues,
            )
            new_user_health_details.save()
            if virtual_assistant_language_id is not None:
                user_language_data = userPreferredVoiceLanguageModel.objects.create(
                    user=UserModel(id=new_user.id),
                    voice_assistant_language=voiceAssistantLanguagesModel(id=virtual_assistant_language_id),
                )
                user_language_data.save()
            generated_referral_code = random_with_N_digits(6)
            new_referral_code = ReferralCodeModel.objects.create(
                user_id=new_user.id,
                referral_code=generated_referral_code,
            )
            new_referral_code.save()
            if(referral_code!=0):
               new_redeem_point = RedeemPointsModel.objects.create(
                   to_user_id=referral_code_data.user.id,
                   from_user_id=new_user.id,
                   redeem_points=25,
                  )
               new_redeem_point.save()
            if 'player_id' != "":
              store_player_id = UserPlayerIdModel.objects.create(
                   user_id=new_user.id,
                   player_id=player_id,
                  )
              store_player_id.save()
            list_of_player_ids = []
            all_admin_users = UserModel.objects.filter(
                       is_admin=True,is_active=True).all()
            for i in range(0,all_admin_users.count()):
              admin_player_id = UserPlayerIdModel.objects.filter(
                       user_id=all_admin_users[i].id,is_active=True).all()
              for j in range(0,admin_player_id.count()):
                 list_of_player_ids.append(admin_player_id[j].player_id)
            print(list_of_player_ids)
            data = {
                 "app_id": os.getenv('ONESIGNAL_APP_ID'),
                 "include_player_ids" : list_of_player_ids,
                 "data": {"foo": f"New user joined recently"},
                 "contents": {"en": "Please check if profile is valid or not"}}           
            R.post(f"{os.getenv('BASE_URL')}/notifications",json=data)
            gmail_account_credentials = UserGoogleSignInModel.objects.create(
                   gmail_id=user_gmail_id,
                   uid=user_uid,
                   user=UserModel(id=new_user.id),
                  )
            gmail_account_credentials.save()
            return Response(
                ResponseData.success_for_referral_code(
                    "Please give sometime to verify your account",generated_referral_code),
                status=status.HTTP_201_CREATED,
            )
        for error in serializer.errors:
            print(serializer.errors[error][0])
        return Response(
            ResponseData.error(serializer.errors[error][0]),
            status=status.HTTP_201_CREATED,
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
        print(f"data {data}")
        if('uid' in request.data):
            google_data = UserGoogleSignInModel.objects.filter(
                uid=data['uid'],is_active=True).first()
            if not google_data:
                return Response(
                    ResponseData.error(
                        "Google account does not exists, please register first"),
                    status=status.HTTP_201_CREATED,
                )
            user_data = UserModel.objects.filter(id=google_data.user_id,is_active=True).first()
            country_details = UserLocationDetailsModel.objects.filter(user_id=google_data.user_id,is_active=True).first()
            country_code = CountriesModel.objects.filter(country_id=country_details.country_id).first()
            country_dial_code=CountriesDialCodeModel.objects.filter(country_code=country_code.country_code).first()
            data['mobile_number'] = str(user_data.mobile_number)
        user = UserModel.objects.filter(Q(mobile_number__icontains=data['mobile_number']),is_active=True).first()
        if not user:
            return Response(
                ResponseData.error(
                    "Account does not exists, please register first"),
                status=status.HTTP_201_CREATED,
            )
        print(request.data)
        country_details = UserLocationDetailsModel.objects.filter(user=UserModel(id=user.id,is_active=True)).first()
        country_code = CountriesModel.objects.filter(country_id=country_details.country_id).first()
        country_dial_code=CountriesDialCodeModel.objects.filter(country_code=country_code.country_code).first()
        data['mobile_number'] = country_dial_code.country_dial_code + str(user.mobile_number)
        playerId = data["player_id"]
        if(user.mobile_number != '+917020829599'):
           if( not user.is_verified):
            return Response(
                ResponseData.error(
                    "Please wait while admin verifies your account"),
                status=status.HTTP_201_CREATED,
            )   
        user_details = UserModel.objects.values().filter(id=user.id,is_active=True).all()
        referral_code = ReferralCodeModel.objects.filter(
            user_id=user_details[0]['id']).first()
        for i in range(0,len(user_details)):
            if(referral_code is not None):
                user_details[i]['referralCode'] = referral_code.referral_code
            user_details[i].pop('created_at')
            user_details[i].pop('updated_at')
        player_id_exists = UserPlayerIdModel.objects.filter(
            user_id=user_details[0]['id'],player_id=playerId).first()
        if player_id_exists:
            player_id_exists.player_id=playerId
            player_id_exists.save()
        else:
            store_player_id = UserPlayerIdModel.objects.create(
               user_id=user_details[0]['id'],
               player_id=playerId,
              )
            store_player_id.save()
        return Response(
                ResponseData.success(
                     user_details,"User logged in successfully"),
            )
            
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@api_view(["POST"])
def is_user_subscribed(request):
    """Function to check if user is subscribed or not"""
    try:
        data = request.data
        serializer = UserSubscribedOrNotSerializer(data=data)
        print(f"IsValid: {serializer.is_valid()}")
        if serializer.is_valid():
            user_id = serializer.data['id']
            user = UserModel.objects.filter(
                id=user_id,is_active=True).first()
            if not user:
                return Response(
                    ResponseData.error(
                        "Account does not exists, please register first"),
                    status=status.HTTP_201_CREATED,
                )
            user_subscription_details = UserPaymentDetailsModel.objects.filter(
                user=UserModel(id=user_id),is_active=True).first()
            if(user_subscription_details is None):
                subscription_data = UserPaymentDetailsModel.objects.filter(
                user=UserModel(id=user_id),subscription__is_free_trial = True).first()
                print(f"subscription_data {subscription_data}")
                if subscription_data is None:
                    return Response(
                        ResponseData.error(
                            "You are not subscribed currently"),
                    status=status.HTTP_201_CREATED)
                return Response(
                    ResponseData.free_trial_subscription_messages(
                        "You free trial subscription is over.",True),
                status=status.HTTP_201_CREATED)
            subscription_data = SubscriptionModel.objects.filter(id=user_subscription_details.subscription_id).first()
            diff = (datetime.now().date() - user_subscription_details.created_at.date())
            if(subscription_data.is_free_trial):
                if(diff.days > int(subscription_data.duration)):
                    print("sxs")
                    # print(diff.days())
                    user_subscription_details.is_active = False
                    user.is_subscribed = False
                    user_subscription_details.save()
                    return JsonResponse(
                      ResponseData.user_subscribed(
                        'User is not subscribed yet. Please make payment first',False,user.is_admin),
                    )
                else:
                  return JsonResponse(
                      ResponseData.user_subscribed(
                        'User is subscribed',True,user.is_admin),
                    )
            elif(subscription_data.is_free_trial == False):
                dateTillSubscriptionIsValid = user_subscription_details.created_at.date() + relativedelta(months=1)
                if(datetime.now().date() > dateTillSubscriptionIsValid):
                    user_subscription_details.is_active = False
                    user_subscription_details.save()
                    return JsonResponse(
                      ResponseData.user_subscribed(
                        'User is not subscribed yet',False,user.is_admin),
                    )
                else:
                 return JsonResponse(
                      ResponseData.user_subscribed(
                        'User is subscribed',True,user.is_admin),
                    )
            else:
                return JsonResponse(
                      ResponseData.user_subscribed(
                        'User is subscribed',True,user.is_admin),
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

class AssignCommitmentForCurrentWeek:
    def day(self, month):
 
        default = "Incorrect day"
 
        return getattr(self, 'case_' + str(month), lambda: default)()
 
    def case_1(self):
        return "3-3-4"
 
    def case_2(self):
        return "2-2-3"
 
    def case_3(self):
        return "2-2-2"

    def case_4(self):
        return "2-2-2"
 
    def case_5(self):
        return "1-1-1"
 
    def case_6(self):
        return "1-1-1"

@api_view(["POST"])
def addNewPayment(request):
    """Function to add new payment done by a user"""
    try:
        data = request.data
        print(data)
        serializer = AddNewPaymentSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            payment_id = serializer.data["payment_id"]
            subscription_id = serializer.data["subscription_id"]
            date_of_payment = serializer.data['date_of_payment']
            subscription_details = SubscriptionModel.objects.filter(
                         id=subscription_id
                     ).first()
            if subscription_details is None:
                        return Response(
                       ResponseData.error("Subscription id is invalid"),
                       status=status.HTTP_200_OK,
                   )
            does_subscription_exists = UserPaymentDetailsModel.objects.filter(
                user_id=user_id,is_active=True).first()
            if does_subscription_exists:
                return Response(
                    ResponseData.error(
                        "You are already subscribed currently"),
                    status=status.HTTP_201_CREATED,
                )
            new_payment_record = UserPaymentDetailsModel.objects.create(
                user_id=user_id,
                payment_id=payment_id,
                subscription_id=subscription_id,
                date_of_payment=date_of_payment,
                is_active = True
            )
            new_payment_record.save()
            user_data = UserModel.objects.filter(id=user_id).first()
            user_data.is_subscribed = True
            user_data.save()
            if user_data.referred_user_code != 0:
                from_user_referral_code = ReferralCodeModel.objects.filter(
                referral_code=user_data.referred_user_code).first()
                if from_user_referral_code is not None:
                    from_user_id = UserModel.objects.filter(id=from_user_referral_code.user_id).first()
                    payment_for_referral_user = PaymentForReferralUsersModel.objects.create(
                        from_user_id=from_user_id,
                        to_user_id=user_data.id,
                        referral_payment_status = ReferralPaymentStatusModel(status='Pending'),
                        amount=30.0
                    )
                    payment_for_referral_user.save()
            current_date = datetime.now().weekday() + 1
            if current_date != 7:
                values = AssignCommitmentForCurrentWeek().day(current_date)
                new_data = UserCommitmentsForNextWeekModel.objects.create(
                    user_id=user_id,
                    min_no_of_food_commitments=str(values).split("-")[0],
                    min_no_of_water_commitments=str(values).split("-")[1],
                    min_no_of_exercise_commitments=str(values).split("-")[2],
                    start_date = datetime.now() + timedelta(days=1),
                    end_date = datetime.now() + timedelta(days=7-current_date)
                )
                new_data.save()
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
def addNewSubscription(request):
    """Function to add new subscription details of a user"""
    try:
        data = request.data
        serializer = AddUserSubscriptionSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            subscription_id = serializer.data["subscription_id"]
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
            does_subscription_exists = UserSubscriptionDetailsModel.objects.filter(
                user_id=user_id,is_active=True).first()
            if does_subscription_exists:
                return Response(
                    ResponseData.error(
                        "You are already subscribed currently"),
                    status=status.HTTP_201_CREATED,
                )
            new_subscription = UserSubscriptionDetailsModel.objects.create(
                user=UserModel(id=user_id),
                subscription_id=subscription_id,
                is_active = True
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
            for i in range(0,subscription_data.count()):
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
            subscription_data = UserSubscriptionDetailsModel.objects.values().filter(user=UserModel(id=user_id),is_active=True).all()
            for i in range(0,subscription_data.count()):
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
        print(request_data)
        user_id = request.data['user_id']
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
        get_all_users = UserModel.objects.values().filter(is_active=True).exclude(id=user_id).all()
        for i in range(0,len(get_all_users)):
            is_relation_there = UserWisePrivacyModel.objects.filter(my_details_id=user_id,other_user_details_id=get_all_users[i]['id']).first()
            if is_relation_there is None:
                new_relation_data = UserWisePrivacyModel.objects.create(
                my_details_id=user_id,
                other_user_details_id=get_all_users[i]['id'],
            )
                new_relation_data.save()
        if(request_data['filterByCategory'] == "" and request_data['filterByDesignation'] == "" and request_data['sortBy'] == "" and search_param == "" ):
           users_data = UserModel.objects.values().filter(is_active=True).order_by('-joining_date').all()[start:end]
        elif(request_data['sortBy'] == "Age (max to min)" and request_data['filterByDesignation'] == ""):
           users_data = UserModel.objects.values().filter(is_active=True).order_by('-userhealthdetailsmodel__age').all()[start:end] if search_param == "" else UserModel.objects.values().filter(Q(full_name__icontains=search_param)| Q(mobile_number__icontains=search_param) | Q(userlocationdetailsmodel__city_name__icontains=search_param),is_active=True).order_by('-userhealthdetailsmodel__age').all()[start:end]
        elif(request_data['sortBy'] == "Age (min to max)" and request_data['filterByDesignation'] == ""):
           users_data = UserModel.objects.values().filter(is_active=True).order_by('userhealthdetailsmodel__age').all()[start:end] if search_param == "" else UserModel.objects.values().filter(Q(full_name__icontains=search_param) | Q(mobile_number__icontains=search_param) | Q(userlocationdetailsmodel__city_name__icontains=search_param),is_active=True).order_by('userhealthdetailsmodel__age').all()[start:end]
        elif(request_data['sortBy'] == "Rank" and request_data['filterByDesignation'] == ""):
           users_data = UserModel.objects.values().filter(is_active=True).order_by('-rank').all()[start:end] if search_param == "" else UserModel.objects.values().filter(Q(full_name__icontains=search_param) | Q(mobile_number__icontains=search_param) | Q(userlocationdetailsmodel__city_name__icontains=search_param),is_active=True).order_by('-rank').all()[start:end]
        elif(request_data['sortBy'] == "Age (max to min)" and request_data['filterByDesignation'] != ""):
           users_data = UserModel.objects.values().filter(userprofessionaldetailsmodel__designation_id = request_data['filterByDesignation'],is_active=True).order_by('-userhealthdetailsmodel__age').all()[start:end] if search_param == "" else UserModel.objects.values().filter(Q(full_name__icontains=search_param)  | Q(mobile_number__icontains=search_param) | Q(userlocationdetailsmodel__city__name__icontains=search_param),is_active=True).filter(userprofessionaldetailsmodel__designation_id=request_data['filterByDesignation']).order_by('-userhealthdetailsmodel__age').all()[start:end]
        elif(request_data['sortBy'] == "Age (min to max)" and request_data['filterByDesignation'] != ""):
           users_data = UserModel.objects.values().filter(userprofessionaldetailsmodel__designation_id = request_data['filterByDesignation'],is_active=True).order_by('userhealthdetailsmodel__age').all()[start:end] if search_param == "" else UserModel.objects.values().filter(Q(full_name__icontains=search_param) | Q(mobile_number__icontains=search_param) | Q(userlocationdetailsmodel__city__name__icontains=search_param),is_active=True).filter(userprofessionaldetailsmodel__designation_id = request_data['filterByDesignation']).order_by('userhealthdetailsmodel__age').all()[start:end]
        elif(request_data['sortBy'] == "Rank" and request_data['filterByDesignation'] != ""):
           users_data = UserModel.objects.values().filter(userprofessionaldetailsmodel__designation_id = request_data['filterByDesignation'],is_active=True).order_by('-rank').all()[start:end] if search_param == "" else UserModel.objects.values().filter(Q(full_name__icontains=search_param) | Q(mobile_number__icontains=search_param) | Q(userlocationdetailsmodel__city__name__icontains=search_param),is_active=True).filter(userprofessionaldetailsmodel__designation_id = request_data['filterByDesignation']).order_by('-rank').all()[start:end]
        elif(request_data['filterByDesignation'] != ""):
           users_data = UserModel.objects.values().filter(userprofessionaldetailsmodel__designation_id = request_data['filterByDesignation'],is_active=True).all()[start:end] if search_param == "" else UserModel.objects.values().filter(Q(full_name__icontains=search_param)  | Q(mobile_number__icontains=search_param) | Q(userlocationdetailsmodel__city__name__icontains=search_param),is_active=True).filter(userprofessionaldetailsmodel__designation_id =request_data['filterByDesignation']).all()[start:end]
        else:
           users_data = UserModel.objects.values().all() if search_param == "" else UserModel.objects.values().filter(Q(full_name__icontains=search_param)| Q(mobile_number__icontains=search_param) | Q(userlocationdetailsmodel__city_name__icontains=search_param),is_active=True).all()
        if(request_data['filterByCategory']) != "" : 
            total_categories = CommitmentCategoryModel.objects.values().filter(name=request_data['filterByCategory']).all()
        else:
            total_categories = CommitmentCategoryModel.objects.values().filter().all()
        for i in range(0,len(users_data)):
            if(len(total_categories) > 1):     
                 commitments_data = CommitmentModel.objects.values().filter(user_id = users_data[i]['id']).all()
                 done_commitments_data = CommitmentModel.objects.values().filter(user_id = users_data[i]['id'],is_done = True,is_updated = True).all()
                 notDone_commitments_data = CommitmentModel.objects.values().filter(user_id = users_data[i]['id'],is_done = False,is_updated = True).all()
                 notUpdated_commitments_data = CommitmentModel.objects.values().filter(user_id = users_data[i]['id'],is_done = False,is_updated = False).all()
                 users_data[i]['commitments_details'] = {}
                 users_data[i]['commitments_details']['total_commitments'] = len(commitments_data)
                 users_data[i]['commitments_details']['total_commitments_done'] = len(done_commitments_data)
                 users_data[i]['commitments_details']['total_commitments_not_done'] = len(notDone_commitments_data)
                 users_data[i]['commitments_details']['total_commitments_not_updated'] = len(notUpdated_commitments_data)
                 users_data[i]['commitments_details']['category_wise'] = []
            for j in range(0,total_categories.count()):
                data = {}
                commitments_data = CommitmentModel.objects.values().filter(user_id = users_data[i]['id'],category = CommitmentCategoryModel(id=total_categories[j]['id'])).all()
                done_commitments_data = CommitmentModel.objects.values().filter(user_id = users_data[i]['id'],category = CommitmentCategoryModel(id=total_categories[j]['id']),is_done = True,is_updated = True).all()
                notDone_commitments_data = CommitmentModel.objects.values().filter(user_id = users_data[i]['id'],category = CommitmentCategoryModel(id=total_categories[j]['id']),is_done = False,is_updated = True).all()
                notUpdated_commitments_data = CommitmentModel.objects.values().filter(user_id = users_data[i]['id'],category = CommitmentCategoryModel(id=total_categories[j]['id']),is_done = False,is_updated = False).all()
                if(total_categories.count() == 1):
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
            city = UserLocationDetailsModel.objects.values().filter(user=UserModel(id=users_data[i]['id'])).first()
            if city is not None:
               users_data[i]['city_data'] = CitiesModel.objects.values().filter(id=city['city_id']).get()
               users_data[i]['city_data'].pop('created_at')
               users_data[i]['city_data'].pop('updated_at')
            income_range_id = UserProfessionalDetailsModel.objects.values().filter(user=UserModel(id=users_data[i]['id'])).first()
            if income_range_id is not None:
               income_data = IncomeModel.objects.values().filter(id=income_range_id['income_range_id']).first()
               if income_data is not None:
                    users_data[i]['income_range_data'] = income_data
                    users_data[i]['income_range_data'].pop('created_at')
                    users_data[i]['income_range_data'].pop('updated_at')
               users_data[i]['designation_data'] = DesignationModel.objects.values().filter(id=income_range_id['designation_id']).get()
               users_data[i]['designation_title'] = income_range_id['designation_title']
               users_data[i]['designation_data'].pop('created_at')
               users_data[i]['designation_data'].pop('updated_at')
            users_data[i]['age'] = UserHealthDetailsModel.objects.values().filter(user=UserModel(id=users_data[i]['id'])).get()['age']
            users_data[i].pop('created_at')
            users_data[i].pop('updated_at')
            users_data[i]['privacy_details'] = {}
            userPrivacyDetails = UserPrivacyModel.objects.values().filter(user_id=users_data[i]['id']).get()
            users_data[i]['privacy_details']['is_age_hidden'] = userPrivacyDetails['is_age_hidden']
            users_data[i]['privacy_details']['is_city_hidden'] = False
            users_data[i]['privacy_details']['is_mobile_number_hidden'] = userPrivacyDetails['is_mobile_number_hidden']
            users_data[i]['privacy_details']['is_designation_title_hidden'] = False
        if(request_data['sortBy'] == 'Commitment done (max to min)'):
            users_data = sorted(users_data, key=lambda d: d['commitments_details']['total_commitments_done'],reverse=True)[start:end]
        elif(request_data['sortBy'] == 'Commitment done (min to max)'):
            users_data = sorted(users_data, key=lambda d: d['commitments_details']['total_commitments_done'],reverse=False)[start:end]
        elif(request_data['filterByCategory'] == "" and request_data['filterByDesignation'] == "" and request_data['sortBy'] == "" and search_param != ""):
            users_data = users_data[start:end]
        if(len(users_data) == 0):
          return Response(
            ResponseData.success(
                users_data, "No Data Found"),
            status=status.HTTP_201_CREATED)
        return Response(
            ResponseData.success(
                users_data, "User Details fetched successfully"),
            status=status.HTTP_201_CREATED)

    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["POST"])
def getAllUnVerifiedUsers(request):
    """Function to get unverified users list"""
    try:
        users_data = UserModel.objects.values().filter(is_verified=False,is_admin=False).order_by('-joining_date').all()
        for i in range(0,len(users_data)):
            city = UserLocationDetailsModel.objects.values().filter(user=UserModel(id=users_data[i]['id'])).get()
            print(city)
            if city is not None:
               users_data[i]['city_data'] = CitiesModel.objects.values().filter(id=city['city_id']).get()
               users_data[i]['city_data'].pop('created_at')
               users_data[i]['city_data'].pop('updated_at')
            income_range_id = UserProfessionalDetailsModel.objects.values().filter(user=UserModel(id=users_data[i]['id'])).get()
            if income_range_id is not None:
               users_data[i]['income_range_data'] = IncomeModel.objects.values().filter(id=income_range_id['income_range_id']).get()
               users_data[i]['designation_data'] = DesignationModel.objects.values().filter(id=income_range_id['designation_id']).get()
               users_data[i]['designation_title'] = income_range_id['designation_title']
               users_data[i]['designation_data'].pop('created_at')
               users_data[i]['designation_data'].pop('updated_at')
               users_data[i]['income_range_data'].pop('created_at')
               users_data[i]['income_range_data'].pop('updated_at')
            users_data[i]['age'] = UserHealthDetailsModel.objects.values().filter(user=UserModel(id=users_data[i]['id'])).get()['age']
            users_data[i].pop('created_at')
            users_data[i].pop('updated_at')
        if(users_data.count() == 0):
          return Response(
            ResponseData.success(
                [], "No unverified user found"),
            status=status.HTTP_201_CREATED)
        return Response(
            ResponseData.success(
                users_data, "Unverified Users list fetched successfully"),
            status=status.HTTP_201_CREATED)

    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["POST"])
def getOverallPerformerOfTheWeek(request):
    """Function to get overall performer of the week"""
    try:
        users_data = UserModel.objects.values().filter(is_active=True).all()
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
            commitment_data = CommitmentModel.objects.values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],is_done = True,is_updated = True).all()
            max_done_commitments['max_commitments'] = len(commitment_data)
            if(len(commitment_data) != 0):
               final_data.append(max_done_commitments)
        newlist = sorted(final_data, key=lambda d: d['max_commitments'],reverse=True)
        user_ids = []
        print(newlist)
        if(len(newlist) > 0):
         user_ids.append(newlist[0]['user_id'])
        for j in range(1,len(newlist)):
                if(str(newlist[j]['max_commitments']) == str(newlist[0]['max_commitments'])):
                    user_ids.append(newlist[j]['user_id'])
        print("called")
        if(len(user_ids) == 0):
          return Response(
            ResponseData.success(
                [], "No Data Found"),
            status=status.HTTP_201_CREATED)
        total_categories = CommitmentCategoryModel.objects.values().filter().all()
        finalData = []
        for k in range(0,len(user_ids)):
            users_data = UserModel.objects.values().filter(id=user_ids[k],is_active=True).all()
            for i in range(0,len(users_data)):
                commitments_data = CommitmentModel.objects.values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id']).all()
                users_data[i]['commitments_details'] = {}
                users_data[i]['commitments_details']['total_commitments'] = commitments_data.count()
                done_commitments_data = CommitmentModel.objects.values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],is_done = True,is_updated = True).all()
                users_data[i]['commitments_details']['total_commitments_done'] = done_commitments_data.count()
                notDone_commitments_data = CommitmentModel.objects.values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],is_done = False,is_updated = True).all()
                users_data[i]['commitments_details']['total_commitments_not_done'] = notDone_commitments_data.count()
                notUpdated_commitments_data = CommitmentModel.objects.values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],is_done = False,is_updated = False).all()
                users_data[i]['commitments_details']['total_commitments_not_updated'] = notUpdated_commitments_data.count()
                users_data[i]['commitments_details']['category_wise'] = []
                for j in range(0,len(total_categories)):
                    data = {}
                    commitments_data = CommitmentModel.objects.values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],category = CommitmentCategoryModel(id=total_categories[j]['id'])).all()
                    data['total_commitments'] = commitments_data.count()
                    done_commitments_data = CommitmentModel.objects.values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],category = CommitmentCategoryModel(id=total_categories[j]['id']),is_done = True,is_updated = True).all()
                    data['total_commitments_done'] = done_commitments_data.count()
                    notDone_commitments_data = CommitmentModel.objects.values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],category = CommitmentCategoryModel(id=total_categories[j]['id']),is_done = False,is_updated = True).all()
                    data['total_commitments_not_done'] = notDone_commitments_data.count()
                    notUpdated_commitments_data = CommitmentModel.objects.values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],category = CommitmentCategoryModel(id=total_categories[j]['id']),is_done = False,is_updated = False).all()
                    data['total_commitments_not_updated'] = notUpdated_commitments_data.count()
                    data['category_name'] = total_categories[j]['name']
                    users_data[i]['commitments_details']['category_wise'].append(data)
                users_data[i].pop('created_at')
                users_data[i].pop('updated_at')
                city_id = UserLocationDetailsModel.objects.values().filter(user=UserModel(id=users_data[i]['id'])).get()
                if city_id is not None:
                  users_data[i]['city_data'] = CitiesModel.objects.values().filter(id=city_id['city_id']).get()
                  users_data[i]['city_data'].pop('created_at')
                  users_data[i]['city_data'].pop('updated_at')
                  income_range_id = UserProfessionalDetailsModel.objects.values().filter(user=UserModel(id=users_data[i]['id'])).get()
                if income_range_id is not None:
                   users_data[i]['income_range_data'] = IncomeModel.objects.values().filter(id=income_range_id['income_range_id']).get()
                   users_data[i]['designation_data'] = DesignationModel.objects.values().filter(id=income_range_id['designation_id']).get()
                   users_data[i]['designation_title'] = income_range_id['designation_title']
                   users_data[i]['designation_data'].pop('created_at')
                   users_data[i]['designation_data'].pop('updated_at')
                   users_data[i]['income_range_data'].pop('created_at')
                   users_data[i]['income_range_data'].pop('updated_at')
                users_data[i]['age'] = UserHealthDetailsModel.objects.values().filter(user=UserModel(id=users_data[i]['id'])).get()['age']
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
def getAllDataOfOverallPerformers(request):
    """Function to get all data of overall performers of all week"""
    try:
        users_data = UserModel.objects.values().filter(is_active=True).all()
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
            commitment_data = CommitmentModel.objects.values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],is_done = True,is_updated = True).all()
            max_done_commitments['max_commitments'] = len(commitment_data)
            if(len(commitment_data) != 0):
               final_data.append(max_done_commitments)
        newlist = sorted(final_data, key=lambda d: d['max_commitments'],reverse=True)
        user_ids = []
        print(newlist)
        if(len(newlist) > 0):
         user_ids.append(newlist[0]['user_id'])
        for j in range(1,len(newlist)):
                if(str(newlist[j]['max_commitments']) == str(newlist[0]['max_commitments'])):
                    user_ids.append(newlist[j]['user_id'])
        print("called")
        if(len(user_ids) == 0):
          return Response(
            ResponseData.success(
                [], "No Data Found"),
            status=status.HTTP_201_CREATED)
        total_categories = CommitmentCategoryModel.objects.values().filter().all()
        finalData = []
        for k in range(0,len(user_ids)):
            users_data = UserModel.objects.values().filter(id=user_ids[k],is_active=True).all()
            for i in range(0,len(users_data)):
                commitments_data = CommitmentModel.objects.values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id']).all()
                users_data[i]['commitments_details'] = {}
                users_data[i]['commitments_details']['total_commitments'] = commitments_data.count()
                done_commitments_data = CommitmentModel.objects.values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],is_done = True,is_updated = True).all()
                users_data[i]['commitments_details']['total_commitments_done'] = done_commitments_data.count()
                notDone_commitments_data = CommitmentModel.objects.values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],is_done = False,is_updated = True).all()
                users_data[i]['commitments_details']['total_commitments_not_done'] = notDone_commitments_data.count()
                notUpdated_commitments_data = CommitmentModel.objects.values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],is_done = False,is_updated = False).all()
                users_data[i]['commitments_details']['total_commitments_not_updated'] = notUpdated_commitments_data.count()
                users_data[i]['commitments_details']['category_wise'] = []
                for j in range(0,len(total_categories)):
                    data = {}
                    commitments_data = CommitmentModel.objects.values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],category = CommitmentCategoryModel(id=total_categories[j]['id'])).all()
                    data['total_commitments'] = commitments_data.count()
                    done_commitments_data = CommitmentModel.objects.values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],category = CommitmentCategoryModel(id=total_categories[j]['id']),is_done = True,is_updated = True).all()
                    data['total_commitments_done'] = done_commitments_data.count()
                    notDone_commitments_data = CommitmentModel.objects.values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],category = CommitmentCategoryModel(id=total_categories[j]['id']),is_done = False,is_updated = True).all()
                    data['total_commitments_not_done'] = notDone_commitments_data.count()
                    notUpdated_commitments_data = CommitmentModel.objects.values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],category = CommitmentCategoryModel(id=total_categories[j]['id']),is_done = False,is_updated = False).all()
                    data['total_commitments_not_updated'] = notUpdated_commitments_data.count()
                    data['category_name'] = total_categories[j]['name']
                    users_data[i]['commitments_details']['category_wise'].append(data)
                users_data[i].pop('created_at')
                users_data[i].pop('updated_at')
                city_id = UserLocationDetailsModel.objects.values().filter(user=UserModel(id=users_data[i]['id'])).get()
                if city_id is not None:
                  users_data[i]['city_data'] = CitiesModel.objects.values().filter(id=city_id['city_id']).get()
                  users_data[i]['city_data'].pop('created_at')
                  users_data[i]['city_data'].pop('updated_at')
                  income_range_id = UserProfessionalDetailsModel.objects.values().filter(user=UserModel(id=users_data[i]['id'])).get()
                if income_range_id is not None:
                   users_data[i]['income_range_data'] = IncomeModel.objects.values().filter(id=income_range_id['income_range_id']).get()
                   users_data[i]['designation_data'] = DesignationModel.objects.values().filter(id=income_range_id['designation_id']).get()
                   users_data[i]['designation_title'] = income_range_id['designation_title']
                   users_data[i]['designation_data'].pop('created_at')
                   users_data[i]['designation_data'].pop('updated_at')
                   users_data[i]['income_range_data'].pop('created_at')
                   users_data[i]['income_range_data'].pop('updated_at')
                users_data[i]['age'] = UserHealthDetailsModel.objects.values().filter(user=UserModel(id=users_data[i]['id'])).get()['age']
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
        all_users_data = UserModel.objects.values().filter(is_active=True).all()
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
                commitment_data = CommitmentModel.objects.values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id =all_users_data[i]['id'],is_done = True,is_updated = True,category = CommitmentCategoryModel(id=total_categories[index]['id'])).all()
                value = len(commitment_data)
                max_done_commitments['max_commitments'] = value
                if(value!=0):
                   final_data.append(max_done_commitments)
            newlist = sorted(final_data, key=lambda d: d['max_commitments'],reverse=True)
            user_ids = []
            if(len(newlist) > 0):
             user_ids.append(newlist[0]['user_id'])
            for j in range(1,len(newlist)):
                    if(str(newlist[j]['max_commitments']) == str(newlist[0]['max_commitments'])):
                        user_ids.append(newlist[j]['user_id'])
            finalData = []
            for k in range(0,len(user_ids)):
                users_data = UserModel.objects.values().filter(id=user_ids[k],is_active=True).all()
                for i in range(0,len(users_data)):
                    commitments_data = CommitmentModel.objects.values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id']).all()
                    users_data[i]['commitments_details'] = {}
                    users_data[i]['commitments_details']['total_commitments'] = commitments_data.count()
                    done_commitments_data = CommitmentModel.objects.values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],is_done = True,is_updated = True).all()
                    users_data[i]['commitments_details']['total_commitments_done'] = done_commitments_data.count()
                    notDone_commitments_data = CommitmentModel.objects.values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],is_done = False,is_updated = True).all()
                    users_data[i]['commitments_details']['total_commitments_not_done'] = notDone_commitments_data.count()
                    notUpdated_commitments_data = CommitmentModel.objects.values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],is_done = False,is_updated = False).all()
                    users_data[i]['commitments_details']['total_commitments_not_updated'] = notUpdated_commitments_data.count()
                    users_data[i]['commitments_details']['category_wise'] = []
                    for j in range(0,len(total_categories)):
                        data = {}
                        commitments_data = CommitmentModel.objects.values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],category = CommitmentCategoryModel(id=total_categories[j]['id'])).all()
                        data['total_commitments'] = commitments_data.count()
                        done_commitments_data_category = CommitmentModel.objects.values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],category = CommitmentCategoryModel(id=total_categories[j]['id']),is_done = True,is_updated = True).all()
                        data['total_commitments_done'] = done_commitments_data_category.count()
                        notDone_commitments_data = CommitmentModel.objects.values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],category = CommitmentCategoryModel(id=total_categories[j]['id']),is_done = False,is_updated = True).all()
                        data['total_commitments_not_done'] = notDone_commitments_data.count()
                        notUpdated_commitments_data = CommitmentModel.objects.values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],category = CommitmentCategoryModel(id=total_categories[j]['id']),is_done = False,is_updated = False).all()
                        data['total_commitments_not_updated'] = notUpdated_commitments_data.count()
                        data['category_name'] = total_categories[j]['name']
                        users_data[i]['commitments_details']['category_wise'].append(data)
                        users_data[i]['category_name'] = total_categories[index]['name']
                users_data[i].pop('created_at')
                users_data[i].pop('updated_at')
                city_id = UserLocationDetailsModel.objects.values().filter(user=UserModel(id=users_data[i]['id'])).get()
                if city_id is not None:
                  users_data[i]['city_data'] = CitiesModel.objects.values().filter(id=city_id['city_id']).get()
                  users_data[i]['city_data'].pop('created_at')
                  users_data[i]['city_data'].pop('updated_at')
                  income_range_id = UserProfessionalDetailsModel.objects.values().filter(user=UserModel(id=users_data[i]['id'])).get()
                if income_range_id is not None:
                   users_data[i]['income_range_data'] = IncomeModel.objects.values().filter(id=income_range_id['income_range_id']).get()
                   users_data[i]['designation_data'] = DesignationModel.objects.values().filter(id=income_range_id['designation_id']).get()
                   users_data[i]['designation_title'] = income_range_id['designation_title']
                   users_data[i]['designation_data'].pop('created_at')
                   users_data[i]['designation_data'].pop('updated_at')
                   users_data[i]['income_range_data'].pop('created_at')
                   users_data[i]['income_range_data'].pop('updated_at')
                users_data[i]['age'] = UserHealthDetailsModel.objects.values().filter(user=UserModel(id=users_data[i]['id'])).get()['age']
                finalData.append(users_data[i])
            for i in range(0,len(finalData)):
               final_next_data.append(finalData[i])
        if(len(final_next_data) == 0):
              return Response(
                ResponseData.success(
                    [], "No winner found"),
                status=status.HTTP_201_CREATED)
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
            print(data)
            user_id = request.data["id"]
            fullName = request.data["fullName"]
            mobile_number = request.data["mobileNumber"]
            email = request.data["email"]
            profilePic = request.FILES['profilePic'] if 'profilePic' in request.FILES else ''
            height = request.data['height']
            weight = request.data["weight"]
            cityName = request.data['cityName']
            stateName = request.data['stateName']
            countryName = request.data['countryName']
            occupationData = request.data["designationData"]
            designationTitle = request.data["designationTitle"]
            userdata = UserModel.objects.filter(
                id=user_id
            ).first()
            if not userdata:
                return Response(
                    ResponseData.error("User id is invalid."),
                    status=status.HTTP_200_OK,
                )
            userdata.full_name=fullName
            userdata.mobile_number=mobile_number
            userdata.email = email
            if 'profilePic' in request.FILES:
                userdata.profile_pic = f"static/{request.FILES['profilePic']}"
            userdata.save()
            if 'profilePic' in request.FILES:
                fs = FileSystemStorage(location='static/')
                fs.save(profilePic.name, profilePic)
            userhealthdata = UserHealthDetailsModel.objects.filter(
                user_id=user_id
            ).first()
            userhealthdata.weight = weight
            userhealthdata.height = height
            userhealthdata.save()
            city_id = CitiesModel.objects.values().filter(name=cityName).get()['id']
            state_id = StatesModel.objects.values().filter(state_name=stateName).get()['state_id']
            country_id = CountriesModel.objects.values().filter(country_name=countryName).get()['country_id']
            userlocationdata = UserLocationDetailsModel.objects.filter(
                user_id=user_id
            ).first()
            userlocationdata.city_id = city_id
            userlocationdata.state_id = state_id
            userlocationdata.country_id = country_id
            userlocationdata.save()
            userdesignationdata = UserProfessionalDetailsModel.objects.filter(
                user_id=user_id
            ).first()
            userdesignationdata.designation_title = designationTitle
            designation_id = DesignationModel.objects.values().filter(title=occupationData).get()['id']
            userdesignationdata.designation_id = designation_id
            userdesignationdata.save()
            updated_date = list(
                UserModel.objects.values().filter(
                    id=user_id)
            )
            return Response(
                ResponseData.success(
                    updated_date[0]['id'], "User profile updated successfully"),
                status=status.HTTP_201_CREATED,
            )
    except KeyError as exception:
        return Response(
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@api_view(["POST"])
def updateUserPrivacyDetails(request):
    """Function to update user privacy details""" 
    try:
        data = request.data
        print(data)
        serializer = UpdateUserPrivacySerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data['user']
            if serializer.data['is_age_hidden'] is not None:
                privacy_details = UserPrivacyModel.objects.filter(user_id=user_id).get()
                privacy_details.is_age_hidden = serializer.data['is_age_hidden']
                privacy_details.save()
            elif serializer.data['is_city_hidden'] is not None:
                privacy_details = UserPrivacyModel.objects.filter(user_id=user_id).get()
                privacy_details.is_city_hidden = serializer.data['is_city_hidden']
                privacy_details.save()
            elif serializer.data['is_mobile_number_hidden'] is not None:
                privacy_details = UserPrivacyModel.objects.filter(user_id=user_id).get()
                privacy_details.is_mobile_number_hidden = serializer.data['is_mobile_number_hidden']
                privacy_details.save()
            elif serializer.data['is_designation_title_hidden'] is not None:
                privacy_details = UserPrivacyModel.objects.filter(user_id=user_id).get()
                privacy_details.is_designation_title_hidden = serializer.data['is_designation_title_hidden']
                privacy_details.save()
            return Response(
                ResponseData.success_without_data(
                    "Details updated successfully"),
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
def updateIndividualUserWisePrivacyDetails(request):
    """Function to update user privacy details for specific user""" 
    try:
        data = request.data
        print(data)
        serializer = UpdateUserPrivacySerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data['user']
            other_user_id = serializer.data['other_user']
            if serializer.data['is_age_hidden'] is not None:
                privacy_details = UserWisePrivacyModel.objects.filter(my_details_id=user_id,other_user_details_id=other_user_id).get()
                privacy_details.is_my_age_hidden = serializer.data['is_age_hidden']
                privacy_details.save()
            elif serializer.data['is_city_hidden'] is not None:
                privacy_details = UserWisePrivacyModel.objects.filter(my_details_id=user_id,other_user_details_id=other_user_id).get()
                privacy_details.is_my_city_hidden = serializer.data['is_city_hidden']
                privacy_details.save()
            elif serializer.data['is_mobile_number_hidden'] is not None:
                privacy_details = UserWisePrivacyModel.objects.filter(my_details_id=user_id,other_user_details_id=other_user_id).get()
                privacy_details.is_my_mobile_number_hidden = serializer.data['is_mobile_number_hidden']
                privacy_details.save()
            elif serializer.data['is_designation_title_hidden'] is not None:
                privacy_details = UserWisePrivacyModel.objects.filter(my_details_id=user_id,other_user_details_id=other_user_id).get()
                privacy_details.is_my_designation_title_hidden = serializer.data['is_designation_title_hidden']
                privacy_details.save()
            return Response(
                ResponseData.success_without_data(
                    "Details updated successfully"),
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
def getUserProfileDetails(request):
    """Function to get user profile details based on user id"""
    try:
        data = request.data
        print(data)
        serializer = GetUserProfileSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["id"]
            user = UserModel.objects.filter(
                id=user_id,is_active=True).first()
            if not user:
                return Response(
                    ResponseData.error(
                        "User id is invalid"),
                    status=status.HTTP_201_CREATED,
                )
            user_details = UserModel.objects.values().filter(id=user_id,is_active=True).all()
            for i in range(0,len(user_details)):
               user_details[i]['total_commitments'] = CommitmentModel.objects.filter(user_id=user_details[i]['id']).count()
               user_details[i]['done_commitments'] = CommitmentModel.objects.filter(user_id=user_details[i]['id'],is_done=True,is_updated=True).count()
               if (user_details[i]['total_commitments']) != 0:
                  user_details[i]['star_rating'] = (user_details[i]['done_commitments']/user_details[i]['total_commitments'])*5
               else:
                  user_details[i]['star_rating'] = 0.0
               users_data = UserModel.objects.values().filter(is_active=True).all()
               for j in range(0,len(users_data)):
                users_data[j]['total_commitments_done'] = CommitmentModel.objects.filter(user_id=users_data[j]['id'],is_done=True,is_updated=True).count()
               users_sorted_data = sorted(users_data, key=lambda d: d['total_commitments_done'],reverse=True)
               for j in range(0,len(users_sorted_data)):
                if(users_sorted_data[j]['id'] == user_id):
                    user_details[i]['user_ranking'] = j+1
                    break
            #    user_details[i]['cashback'] = UserCashbackModel.objects.values().filter(user_id=user_details[i]['id']).get().amount
            #    giveCashbackToUser()
               user_details[i]['cashback'] = 0.0
               user_details[i].pop('created_at')
               user_details[i].pop('updated_at')
               user_details[i].pop('is_active')
               user_health_details = UserHealthDetailsModel.objects.values().filter(user=UserModel(id=user_details[i]['id'])).get()
               if user_health_details is not None:
                 user_details[i]['age'] = user_health_details['age']
                 user_details[i]['weight'] = user_health_details['weight']
                 user_details[i]['height'] = user_health_details['height']
                 user_details[i]['gender'] = user_health_details['gender']
               user_subscription_details = UserPaymentDetailsModel.objects.filter(
                user=UserModel(id=user_details[i]['id']),is_active=True).first()
               subscription_data = SubscriptionModel.objects.filter(id=user_subscription_details.subscription_id).first()
               user_details[i]['is_free_trial'] = subscription_data.is_free_trial
               city_id = UserLocationDetailsModel.objects.values().filter(user=UserModel(id=user_details[i]['id'])).get()
               if city_id is not None:
                user_details[i]['city_name'] = CitiesModel.objects.values().filter(id=city_id['city_id']).get()['name']
               state_id = UserLocationDetailsModel.objects.values().filter(user=UserModel(id=user_details[i]['id'])).get()
               if state_id is not None:
                user_details[i]['state_name'] = StatesModel.objects.values().filter(state_id=state_id['state_id']).get()['state_name']
               country_id = UserLocationDetailsModel.objects.values().filter(user=UserModel(id=user_details[i]['id'])).get()
               if country_id is not None:
                user_details[i]['country_name'] = CountriesModel.objects.values().filter(country_id=country_id['country_id']).get()['country_name']
               income_range_id = UserProfessionalDetailsModel.objects.values().filter(user=UserModel(id=user_details[i]['id'])).get()
               if income_range_id['income_range_id'] is not None:
                user_details[i]['income_range_data'] = IncomeModel.objects.values().filter(id=income_range_id['income_range_id']).get()['income_range']
                user_details[i]['designation_data'] = DesignationModel.objects.values().filter(id=income_range_id['designation_id']).get()['title']
                user_details[i]['designation_title'] = income_range_id['designation_title']
               check_data = RedeemPointsModel.objects.values().filter().all()
               for j in range(0,check_data.count()):
                  if(check_data[j]['to_user_id'] == user_id and check_data[j]['is_active']):
                   user_details[i]['redeem_point_data'] = check_data[j]
                   user_details[i]['redeem_point_data'].pop('updated_at')
                   user_details[i]['redeem_point_data'].pop('created_at')
                   user_details[i]['redeem_point_data'].pop('from_user_id')
            print(user_details)
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

@api_view(["POST"])
def getUserPrivacyDetails(request):
    """Function to get user privacy details"""
    try:
        data = request.data
        print(data)
        serializer = GetUserProfileSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["id"]
            user = UserModel.objects.filter(
                id=user_id,is_active=True).first()
            if not user:
                return Response(
                    ResponseData.error(
                        "User id is invalid"),
                    status=status.HTTP_201_CREATED,
                )
            user_privacy_details = UserPrivacyModel.objects.values().filter(user_id=user_id).all()
            for i in range(0,len(user_privacy_details)):
                user_privacy_details[0].pop('created_at')
                user_privacy_details[0].pop('updated_at')
            return Response(
                ResponseData.success(
                    user_privacy_details, " Privacy details fetched successfully"),
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
def getIndividualUserWisePrivacyDetails(request):
    """Function to get user privacy details for individual user wise"""
    try:
        data = request.data
        print(data)
        serializer = GetUserProfileSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["id"]
            other_user_id = serializer.data['other_user_id']
            user = UserModel.objects.filter(
                id=user_id,is_active=True).first()
            if not user:
                return Response(
                    ResponseData.error(
                        "User id is invalid"),
                    status=status.HTTP_201_CREATED,
                )
            user_privacy_details = UserWisePrivacyModel.objects.values().filter(my_details_id=user_id,other_user_details_id=other_user_id).all()
            for i in range(0,len(user_privacy_details)):
                user_privacy_details[0].pop('created_at')
                user_privacy_details[0].pop('updated_at')
            return Response(
                ResponseData.success(
                    user_privacy_details, " Privacy details fetched successfully"),
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
def makeUserAdmin(request):
    """Function to make a user admin"""
    try:
        data = request.data
        serializer = GetUserProfileSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["id"]
            user = UserModel.objects.filter(
                id=user_id,is_active=True).first()
            if not user:
                return Response(
                    ResponseData.error(
                        "User id is invalid"),
                    status=status.HTTP_201_CREATED,
                )
            user.is_admin = True
            user.save()
            return Response(
                ResponseData.success(
                    [], "User has become admin now"),
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
def delete_user_details(request):
    """Function to delete user details"""
    try:
        data = request.data
        user_id = data["user_id"]
        is_id_valid = UserModel.objects.filter(id=user_id).first()
        CommitmentModel.objects.filter(user_id=user_id).delete()
        if not is_id_valid:
               return Response(
                   ResponseData.error("User id is invalid"),
                   status=status.HTTP_200_OK,
               )
        UserSubscriptionDetailsModel.objects.filter(user_id=user_id).delete()
        UserPaymentDetailsModel.objects.filter(user_id=user_id).delete()
        UserGoogleSignInModel.objects.filter(user_id=user_id).delete()
        UserLocationDetailsModel.objects.filter(user_id=user_id).delete()
        UserProfessionalDetailsModel.objects.filter(user_id=user_id).delete()
        UserHealthDetailsModel.objects.filter(user_id=user_id).delete()
        RedeemPointsModel.objects.filter(from_user_id=user_id).delete()
        ReferralCodeModel.objects.filter(user_id=user_id).delete()
        UserModel.objects.filter(id=user_id).delete()
        return Response(
            ResponseData.success_without_data("User details deleted successfully"),
            status=status.HTTP_201_CREATED)
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

from twilio.rest import Client

# account_sid = 'ACe0c13b45f4486432ca3eea5759905960'
# auth_token = 'be2aab1bab8b7e6c650aeafe6bdd711a'
# client = Client(account_sid, auth_token)

# call = client.calls.create(
#                         twiml='<Response><Say>Hey anirudh, today is best day for you in your life. Please get up.</Say></Response>',
#                         to='+917020829599',
#                         from_='+19704323190'
#                     )

# print(call.sid)

@api_view(["POST"])
def addNewReviewOfUser(request):
    """Function to add new review given by a user"""
    try:
        data = request.data
        print(data)
        serializer = AddUserReviewSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            data_of_all_reviews = serializer.data["data_of_all_reviews"]
            user_details = UserModel.objects.filter(
                         id=user_id
                     ).first()
            if user_details is None:
                        return Response(
                       ResponseData.error("User id is invalid"),
                       status=status.HTTP_200_OK,
                   )
            final_data = []
            for i in range(0,len(data_of_all_reviews)):
                review_details = ReviewModel.objects.filter(
                             id=data_of_all_reviews[i]['review_id']
                         ).first()
                if review_details is None:
                            return Response(
                           ResponseData.error("Review id is invalid"),
                           status=status.HTTP_200_OK,
                       )
                does_data_exists = UserReviewModel.objects.filter(
                             user_id=user_id,
                    review_date = str(data_of_all_reviews[i]['review_date']).split("T")[0]
                         ).first()
                if does_data_exists is not None:
                        return Response(
                           ResponseData.error("This data already exists"),
                           status=status.HTTP_200_OK,
                       )
                final_data.append(UserReviewModel(
                    user_id=user_id,
                    review_id=data_of_all_reviews[i]['review_id'],
                    star_rating=data_of_all_reviews[i]['star_rating'],
                    description=data_of_all_reviews[i]['description'],
                    review_date = str(data_of_all_reviews[i]['review_date']).split("T")[0]
                ))
            print(f"final_data {final_data}")
            UserReviewModel.objects.bulk_create(final_data)
            return Response(
                    ResponseData.success_without_data(
                        "Review added successfully"),
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
def updateUserReview(request):
    """Function to update review details of user""" 
    try:
        data = request.data
        print(data)
        serializer = UpdateUserReviewSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            review_id = serializer.data["review_id"]
            star_rating = serializer.data["star_rating"]
            description = serializer.data['description']
            user_review_id = serializer.data['user_review_id']
            user_review_details = UserReviewModel.objects.filter(
                         id=user_review_id
                     ).first()
            if user_review_details is None:
                        return Response(
                       ResponseData.error("User review id is invalid"),
                       status=status.HTTP_200_OK,
                   )
            user_details = UserModel.objects.filter(
                         id=user_id
                     ).first()
            if user_details is None:
                        return Response(
                       ResponseData.error("User id is invalid"),
                       status=status.HTTP_200_OK,
                   )
            review_details = ReviewModel.objects.filter(
                         id=review_id
                     ).first()
            if review_details is None:
                        return Response(
                       ResponseData.error("Review id is invalid"),
                       status=status.HTTP_200_OK,
                   )
            user_review_details.star_rating = star_rating
            user_review_details.description = description
            user_review_details.updated_at = datetime.now()
            user_review_details.save()
            return Response(
                ResponseData.success_without_data(
                    "Review updated successfully"),
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
def deleteUserReview(request):
    """Function to delete user review"""
    try:
        data = request.data
        user_review_id = data["user_review_id"]
        is_id_valid = UserReviewModel.objects.filter(id=user_review_id).first()
        if not is_id_valid:
               return Response(
                   ResponseData.error("User review id is invalid"),
                   status=status.HTTP_200_OK,
               )
        UserReviewModel.objects.filter(id=user_review_id).delete()
        return Response(
            ResponseData.success_without_data("User details deleted successfully"),
            status=status.HTTP_201_CREATED)
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["POST"])
def get_reviews_of_all_users(request):
    """Function to get reviews of all users"""
    try:
        data = request.data
        print(data)
        serializer = GetReviewsOfAllUsersSerializer(data=data)
        if serializer.is_valid():
            page_number = int(serializer.data['page_no'] if 'page_no' in request.data else 0)
            page_size_param = int(serializer.data['page_size'] if 'page_size' in request.data else 0)
            star_rating = serializer.data['star_rating'] if 'star_rating' in request.data else ""
            search = serializer.data['search'] if 'search' in request.data else ""
            start_date = serializer.data['start_date'] if 'start_date' in request.data else ""
            end_date = serializer.data['end_date'] if 'end_date' in request.data else ""
            page_no = page_number
            page_size = page_size_param
            if star_rating != "":
                start_rating = int(str(star_rating).split("-")[0])
                end_rating = int(str(star_rating).split("-")[1])
            start=(page_no-1)*page_size
            end=page_no*page_size
            get_users_id = UserReviewModel.objects.values_list('user_id').distinct()[start:end]
            final_data = []
            print(f"get_users_id {get_users_id}")
            for i in range(0,len(get_users_id)):
                if star_rating != "" and search == "" and start_date == '':
                    user_reviews_data = UserReviewModel.objects.values().filter(user_id=get_users_id[i][0]).filter(Q(star_rating__range=[start_rating, end_rating])).all()
                elif star_rating != "" and search == "" and start_date != '':
                    user_reviews_data = UserReviewModel.objects.values().filter(Q(review_date__range=[start_date, end_date]) & Q(star_rating__range=[start_rating, end_rating])).filter(user_id=get_users_id[i][0]).all()
                elif star_rating != "" and search != "" and start_date == '':
                    user_reviews_data = UserReviewModel.objects.values().filter((Q(user__full_name__icontains=search) | Q(user__mobile_number__icontains=search) | Q(description__icontains=search)) & (Q(star_rating__range=[start_rating, end_rating]))).filter(user_id=get_users_id[i][0]).all()
                elif star_rating != "" and search != "" and start_date != '':
                    user_reviews_data = UserReviewModel.objects.values().filter((Q(user__full_name__icontains=search) | Q(user__mobile_number__icontains=search) | Q(description__icontains=search)) & (Q(star_rating__range=[start_rating, end_rating]))).filter(Q(review_date__range=[start_date, end_date])).filter(user_id=get_users_id[i][0]).all()
                elif star_rating == "" and search != "" and start_date == '':
                    user_reviews_data = UserReviewModel.objects.values().filter(Q(user__full_name__icontains=search) | Q(user__mobile_number__icontains=search) | Q(description__icontains=search)).filter(user_id=get_users_id[i][0]).all()
                elif star_rating == "" and search != "" and start_date != '':
                    user_reviews_data = UserReviewModel.objects.values().filter(Q(user__full_name__icontains=search) | Q(user__mobile_number__icontains=search) | Q(description__icontains=search)).filter(Q(review_date__range=[start_date, end_date])).filter(user_id=get_users_id[i][0]).all()
                elif star_rating == "" and search == "" and start_date != '':
                    user_reviews_data = UserReviewModel.objects.values().filter(Q(review_date__range=[start_date, end_date])).filter(user_id=get_users_id[i][0]).all()
                else:
                    user_reviews_data = UserReviewModel.objects.values().filter(user_id=get_users_id[i][0]).all()
                for j in range(0,len(user_reviews_data)):
                    # user_reviews_data[j].pop("created_at")
                    # user_reviews_data[j].pop("updated_at")
                    # user_reviews_data[j].pop("user_id")
                    user_reviews_data[j]['review_title'] = ReviewModel.objects.values().filter(id=user_reviews_data[j]['review_id']).first()['title']
                    # user_reviews_data[j].pop("review_id")
                map = {}
                if len(user_reviews_data) > 0:
                    user_data = UserModel.objects.filter(id=get_users_id[i][0]).first()
                    if user_data is not None:
                        print(f"get_users_id[i][0] {get_users_id[i][0]}")
                        map['user_name'] = user_data.full_name
                        map['review_data'] = user_reviews_data
                        final_data.append(map)
            if len(final_data) == 0:
                    return Response(
                       ResponseData.success(
                           [], "No user review found"),
                       status=status.HTTP_201_CREATED)
            return Response(
                       ResponseData.success(
                           final_data, "User Reviews fetched successfully"),
                       status=status.HTTP_201_CREATED)
        return Response(
                    ResponseData.error(serializer.errors),
                    status=status.HTTP_400_BAD_REQUEST,
                )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
