from rest_framework.decorators import api_view
from location.models import CitiesModel, CountriesDialCodeModel
from commitment.models import CommitmentCategoryModel, CommitmentModel
from designation.models import DesignationModel
from income.models import IncomeModel
from location.models import CountriesModel, StatesModel
from notifications.models import UserPlayerIdModel
from notifications.views import send_notification_to_admin
from onesignal import BASE_URL, ONESIGNAL_APP_ID
from redeemPoints.models import RedeemPointsModel
from referralCode.models import ReferralCodeModel
from subscription.models import SubscriptionModel
from user.models import UserGoogleSignInModel, UserHealthDetailsModel, UserLocationDetailsModel, UserModel, UserPaymentDetailsModel, UserProfessionalDetailsModel, UserSubscriptionDetailsModel
from rest_framework.response import Response
from user.serializers import AddNewPaymentSerializer, AddUserSubscriptionSerializer, GetUserProfileSerializer, GetUserSubscriptionSerializer, UserSignInSerializer, UserSignUpSerializer, UserSubscribedOrNotSerializer
from django.core.files.storage import FileSystemStorage
from response import Response as ResponseData
from rest_framework import status
from django.http.response import JsonResponse
from datetime import *
from django.db.models import Q
from random import randint
import requests as R
from dateutil.relativedelta import relativedelta

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
            income_range = serializer.data['income_range']
            is_medicine_ongoing = serializer.data['is_medicine_ongoing']
            any_health_issues = serializer.data['any_health_issues']
            player_id = serializer.data['player_id'] if 'player_id' in request.data else ""
            user_uid = serializer.data['user_uid'] if 'user_uid' in request.data else ""
            user_gmail_id = serializer.data['user_gmail_id'] if 'user_gmail_id' in request.data else ""
            user = UserModel.objects.using('user_db').filter(
                Q(email__icontains=email) | Q(mobile_number__icontains=mobile_number)).first()
            if user:
                return Response(
                    ResponseData.error(
                        "User is already registered please log in"),
                    status=status.HTTP_201_CREATED,
                )
            if(referral_code!=0):
              referral_code_data = ReferralCodeModel.objects.using('referralCode_db').filter(
                  referral_code=referral_code).all()
              if referral_code_data.count() == 0:
                  return Response(
                      ResponseData.error(
                          "Referral code is invalid"),
                      status=status.HTTP_201_CREATED,
                  )
            if profile_pic!="":
                 fs = FileSystemStorage(location='static/')
                 fs.save(profile_pic.name, profile_pic)
            new_user = UserModel.objects.using('user_db').create(
                full_name=full_name,
                mobile_number=mobile_number,
                email=email,
                profile_pic= "" if profile_pic == "" else f"static/{profile_pic}",
                password=password,
                birth_date=birth_date,
                is_verified = True if mobile_number == "+917020829599" else False,
                is_admin = True if mobile_number == "+917020829599" else False,
                is_active=True if mobile_number == "+917020829599" else False,
            )
            new_user.save()
            city_name = CitiesModel.objects.using('location_db').filter(id=city_id).first()
            new_user_location = UserLocationDetailsModel.objects.using('user_db').create(
                user_id=new_user.id,
                city_id=city_id,
                state_id=state_id,
                country_id=country_id, 
                city_name=city_name.name
            )
            new_user_location.save()
            new_user_professional_details = UserProfessionalDetailsModel.objects.using('user_db').create(
                designation_title=designation_title,
                user=UserModel(id=new_user.id),
                designation_id=designation,
                income_range_id=income_range,
            )
            new_user_professional_details.save()
            new_user_health_details = UserHealthDetailsModel.objects.using('user_db').create(
                user=UserModel(id=new_user.id),
                weight=weight,
                height=height,
                gender=gender,
                age=age,
                is_medicine_ongoing=is_medicine_ongoing,
                any_health_issues=any_health_issues,
            )
            new_user_health_details.save()
            generated_referral_code = random_with_N_digits(6)
            new_referral_code = ReferralCodeModel.objects.using('referralCode_db').create(
                user_id=new_user.id,
                referral_code=generated_referral_code,
            )
            new_referral_code.save()
            if(referral_code!=0):
               new_redeem_point = RedeemPointsModel.objects.using('redeemPoints_db').create(
                   to_user_id=referral_code_data[0].user.id,
                   from_user_id=new_user.id,
                   redeem_points=25,
                  )
               new_redeem_point.save()
            if 'player_id' != "":
              store_player_id = UserPlayerIdModel.objects.using('notifications_db').create(
                   user_id=new_user.id,
                   player_id=player_id,
                  )
              store_player_id.save()
            list_of_player_ids = []
            all_admin_users = UserModel.objects.using('user_db').filter(
                       is_admin=True,is_active=True).all()
            for i in range(0,all_admin_users.count()):
              admin_player_id = UserPlayerIdModel.objects.using('notifications_db').filter(
                       user_id=all_admin_users[i].id,is_active=True).all()
              for j in range(0,admin_player_id.count()):
                 list_of_player_ids.append(admin_player_id[j].player_id)
            print(list_of_player_ids)
            data = {
                 "app_id": ONESIGNAL_APP_ID,
                 "include_player_ids" : list_of_player_ids,
                 "data": {"foo": f"New user joined recently"},
                 "contents": {"en": "Please check if profile is valid or not"}}           
            R.post(f"{BASE_URL}/notifications",json=data)
            gmail_account_credentials = UserGoogleSignInModel.objects.using('user_db').create(
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
            google_data = UserGoogleSignInModel.objects.using('user_db').filter(
                uid=data['uid'],is_active=True).first()
            if not google_data:
                return Response(
                    ResponseData.error(
                        "Google account does not exists, please register first"),
                    status=status.HTTP_201_CREATED,
                )
            user_data = UserModel.objects.using('user_db').filter(id=google_data.user_id,is_active=True).first()
            country_details = UserLocationDetailsModel.objects.using('user_db').filter(user_id=google_data.user_id,is_active=True).first()
            country_code = CountriesModel.objects.using('location_db').filter(country_id=country_details.country_id).first()
            country_dial_code=CountriesDialCodeModel.objects.using('location_db').filter(country_code=country_code.country_code).first()
            data['mobile_number'] = str(user_data.mobile_number)
        user = UserModel.objects.using('user_db').filter(Q(mobile_number__icontains=data['mobile_number']),is_active=True).first()
        if not user:
            return Response(
                ResponseData.error(
                    "Account does not exists, please register first"),
                status=status.HTTP_201_CREATED,
            )
        print(request.data)
        country_details = UserLocationDetailsModel.objects.using('user_db').filter(user=UserModel(id=user.id,is_active=True)).first()
        country_code = CountriesModel.objects.using('location_db').filter(country_id=country_details.country_id).first()
        country_dial_code=CountriesDialCodeModel.objects.using('location_db').filter(country_code=country_code.country_code).first()
        data['mobile_number'] = country_dial_code.country_dial_code + str(user.mobile_number)
        playerId = data["player_id"]
        if(user.mobile_number != '+917020829599'):
           if( not user.is_verified):
            return Response(
                ResponseData.error(
                    "Please wait while admin verifies your account"),
                status=status.HTTP_201_CREATED,
            )   
        user_details = UserModel.objects.using('user_db').values().filter(id=user.id,is_active=True).all()
        referral_code = ReferralCodeModel.objects.using('referralCode_db').filter(
            user_id=user_details[0]['id']).first()
        for i in range(0,len(user_details)):
            user_details[i]['referralCode'] = referral_code.referral_code
            user_details[i].pop('created_at')
            user_details[i].pop('updated_at')
        player_id_exists = UserPlayerIdModel.objects.using('notifications_db').filter(
            user_id=user_details[0]['id'],player_id=playerId).first()
        if player_id_exists:
            player_id_exists.player_id=playerId
            player_id_exists.save()
        else:
            store_player_id = UserPlayerIdModel.objects.using('notifications_db').create(
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
            user = UserModel.objects.using('user_db').filter(
                id=user_id,is_active=True).first()
            if not user:
                return Response(
                    ResponseData.error(
                        "Account does not exists, please register first"),
                    status=status.HTTP_201_CREATED,
                )
            user_subscription_details = UserPaymentDetailsModel.objects.using('user_db').filter(
                user=UserModel(id=user_id),is_active=True).first()
            if(user_subscription_details is None):
                return Response(
                    ResponseData.error(
                        "You are not subscribed currently"),
                status=status.HTTP_201_CREATED)
            subscription_data = SubscriptionModel.objects.using('subscription_db').filter(id=user_subscription_details.subscription_id).first()
            diff = (datetime.now().date() - user_subscription_details.created_at.date())
            print(subscription_data.is_free_trial)
            if(subscription_data.is_free_trial):
                if(diff.days > int(subscription_data.duration)):
                    print(diff.days())
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

@api_view(["POST"])
def addNewPayment(request):
    """Function to add new payment done by a user"""
    try:
        data = request.data
        print(data)
        serializer = AddNewPaymentSerializer(data=data)
        if serializer.is_valid():
            print("dcds")
            user_id = serializer.data["user_id"]
            payment_id = serializer.data["payment_id"]
            subscription_id = serializer.data["subscription_id"]
            date_of_payment = serializer.data['date_of_payment']
            subscription_details = SubscriptionModel.objects.using('subscription_db').filter(
                         id=subscription_id
                     ).first()
            if subscription_details is None:
                        return Response(
                       ResponseData.error("Subscription id is invalid"),
                       status=status.HTTP_200_OK,
                   )
            does_subscription_exists = UserPaymentDetailsModel.objects.using('user_db').filter(
                user_id=user_id,is_active=True).first()
            if does_subscription_exists:
                return Response(
                    ResponseData.error(
                        "You are already subscribed currently"),
                    status=status.HTTP_201_CREATED,
                )
            new_payment_record = UserPaymentDetailsModel.objects.using('user_db').create(
                user_id=user_id,
                payment_id=payment_id,
                subscription_id=subscription_id,
                date_of_payment=date_of_payment,
                is_active = True
            )
            new_payment_record.save()
            # new_subscription = UserSubscriptionDetailsModel.objects.using('user_db').create(
            #     user=UserModel(id=user_id),
            #     subscription_id=subscription_id,
            #     is_active = True
            # )
            # new_subscription.save()
            user_data = UserModel.objects.using('user_db').filter(id=user_id).first()
            print("dcdssdcs")
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
            user_id = serializer.data["user_id"]
            subscription_id = serializer.data["subscription_id"]
            user = UserModel.objects.using('user_db').filter(
                id=user_id).first()
            if not user:
                return Response(
                    ResponseData.error(
                        "User id is invalid"),
                    status=status.HTTP_201_CREATED,
                )
            subscription = SubscriptionModel.objects.using('subscription_db').filter(
                id=subscription_id).first()
            if not subscription:
                return Response(
                    ResponseData.error(
                        "Subscription id is invalid"),
                    status=status.HTTP_201_CREATED,
                )
            does_subscription_exists = UserSubscriptionDetailsModel.objects.using('user_db').filter(
                user_id=user_id,is_active=True).first()
            if does_subscription_exists:
                return Response(
                    ResponseData.error(
                        "You are already subscribed currently"),
                    status=status.HTTP_201_CREATED,
                )
            new_subscription = UserSubscriptionDetailsModel.objects.using('user_db').create(
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
            user = UserModel.objects.using('user_db').filter(
                id=user_id).first()
            if not user:
                return Response(
                    ResponseData.error(
                        "User id is invalid"),
                    status=status.HTTP_201_CREATED,
                )
            subscription = SubscriptionModel.objects.using('subscription_db').filter(
                id=subscription_id).first()
            if not subscription:
                return Response(
                    ResponseData.error(
                        "Subscription id is invalid"),
                    status=status.HTTP_201_CREATED,
                )
            subscription_data = UserSubscriptionDetailsModel.objects.using('user_db').values().filter(id=subscription_id,user=UserModel(id=user_id)).all()
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
            user = UserModel.objects.using('user_db').filter(
                id=user_id).first()
            if not user:
                return Response(
                    ResponseData.error(
                        "User id is invalid"),
                    status=status.HTTP_201_CREATED,
                )
            subscription_data = UserSubscriptionDetailsModel.objects.using('user_db').values().filter(user=UserModel(id=user_id),is_active=True).all()
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
        if(request_data['filterByCategory'] == "" and request_data['filterByDesignation'] == "" and request_data['sortBy'] == "" and search_param == "" ):
           users_data = UserModel.objects.using('user_db').values().filter(is_active=True).order_by('-joining_date').all()[start:end]
        elif(request_data['sortBy'] == "Age (max to min)" and request_data['filterByDesignation'] == ""):
           users_data = UserModel.objects.using('user_db').values().filter(is_active=True).order_by('-userhealthdetailsmodel__age').all()[start:end] if search_param == "" else UserModel.objects.using('user_db').values().filter(Q(full_name__icontains=search_param)| Q(mobile_number__icontains=search_param) | Q(userlocationdetailsmodel__city_name__icontains=search_param),is_active=True).order_by('-userhealthdetailsmodel__age').all()[start:end]
        elif(request_data['sortBy'] == "Age (min to max)" and request_data['filterByDesignation'] == ""):
           users_data = UserModel.objects.using('user_db').values().filter(is_active=True).order_by('userhealthdetailsmodel__age').all()[start:end] if search_param == "" else UserModel.objects.using('user_db').values().filter(Q(full_name__icontains=search_param) | Q(mobile_number__icontains=search_param) | Q(userlocationdetailsmodel__city_name__icontains=search_param),is_active=True).order_by('userhealthdetailsmodel__age').all()[start:end]
        elif(request_data['sortBy'] == "Age (max to min)" and request_data['filterByDesignation'] != ""):
           users_data = UserModel.objects.using('user_db').values().filter(userprofessionaldetailsmodel__designation_id = request_data['filterByDesignation'],is_active=True).order_by('-userhealthdetailsmodel__age').all()[start:end] if search_param == "" else UserModel.objects.using('user_db').values().filter(Q(full_name__icontains=search_param)  | Q(mobile_number__icontains=search_param) | Q(userlocationdetailsmodel__city__name__icontains=search_param),is_active=True).filter(userprofessionaldetailsmodel__designation_id=request_data['filterByDesignation']).order_by('-userhealthdetailsmodel__age').all()[start:end]
        elif(request_data['sortBy'] == "Age (min to max)" and request_data['filterByDesignation'] != ""):
           users_data = UserModel.objects.using('user_db').values().filter(userprofessionaldetailsmodel__designation_id = request_data['filterByDesignation'],is_active=True).order_by('userhealthdetailsmodel__age').all()[start:end] if search_param == "" else UserModel.objects.using('user_db').values().filter(Q(full_name__icontains=search_param) | Q(mobile_number__icontains=search_param) | Q(userlocationdetailsmodel__city__name__icontains=search_param),is_active=True).filter(userprofessionaldetailsmodel__designation_id = request_data['filterByDesignation']).order_by('userhealthdetailsmodel__age').all()[start:end]
        elif(request_data['filterByDesignation'] != ""):
           users_data = UserModel.objects.using('user_db').values().filter(userprofessionaldetailsmodel__designation_id = request_data['filterByDesignation'],is_active=True).all()[start:end] if search_param == "" else UserModel.objects.using('user_db').values().filter(Q(full_name__icontains=search_param)  | Q(mobile_number__icontains=search_param) | Q(userlocationdetailsmodel__city__name__icontains=search_param),is_active=True).filter(userprofessionaldetailsmodel__designation_id =request_data['filterByDesignation']).all()[start:end]
        else:
           users_data = UserModel.objects.using('user_db').values().all() if search_param == "" else UserModel.objects.using('user_db').values().filter(Q(full_name__icontains=search_param)| Q(mobile_number__icontains=search_param) | Q(userlocationdetailsmodel__city_name__icontains=search_param),is_active=True).all()
        if(request_data['filterByCategory']) != "" : 
            total_categories = CommitmentCategoryModel.objects.using('commitment_db').values().filter(name=request_data['filterByCategory']).all()
        else:
            total_categories = CommitmentCategoryModel.objects.using('commitment_db').values().filter().all()
        for i in range(0,len(users_data)):
            if(total_categories.count() > 1):     
                 commitments_data = CommitmentModel.objects.using('commitment_db').values().filter(user_id = users_data[i]['id']).all()
                 done_commitments_data = CommitmentModel.objects.using('commitment_db').values().filter(user_id = users_data[i]['id'],is_done = True,is_updated = True).all()
                 notDone_commitments_data = CommitmentModel.objects.using('commitment_db').values().filter(user_id = users_data[i]['id'],is_done = False,is_updated = True).all()
                 notUpdated_commitments_data = CommitmentModel.objects.using('commitment_db').values().filter(user_id = users_data[i]['id'],is_done = False,is_updated = False).all()
                 users_data[i]['commitments_details'] = {}
                 users_data[i]['commitments_details']['total_commitments'] = len(commitments_data)
                 users_data[i]['commitments_details']['total_commitments_done'] = len(done_commitments_data)
                 users_data[i]['commitments_details']['total_commitments_not_done'] = len(notDone_commitments_data)
                 users_data[i]['commitments_details']['total_commitments_not_updated'] = len(notUpdated_commitments_data)
                 users_data[i]['commitments_details']['category_wise'] = []
            for j in range(0,total_categories.count()):
                data = {}
                commitments_data = CommitmentModel.objects.using('commitment_db').values().filter(user_id = users_data[i]['id'],category = CommitmentCategoryModel(id=total_categories[j]['id'])).all()
                done_commitments_data = CommitmentModel.objects.using('commitment_db').values().filter(user_id = users_data[i]['id'],category = CommitmentCategoryModel(id=total_categories[j]['id']),is_done = True,is_updated = True).all()
                notDone_commitments_data = CommitmentModel.objects.using('commitment_db').values().filter(user_id = users_data[i]['id'],category = CommitmentCategoryModel(id=total_categories[j]['id']),is_done = False,is_updated = True).all()
                notUpdated_commitments_data = CommitmentModel.objects.using('commitment_db').values().filter(user_id = users_data[i]['id'],category = CommitmentCategoryModel(id=total_categories[j]['id']),is_done = False,is_updated = False).all()
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
            city = UserLocationDetailsModel.objects.using('user_db').values().filter(user=UserModel(id=users_data[i]['id'])).first()
            if city is not None:
               users_data[i]['city_data'] = CitiesModel.objects.using('location_db').values().filter(id=city['city_id']).get()
               users_data[i]['city_data'].pop('created_at')
               users_data[i]['city_data'].pop('updated_at')
            income_range_id = UserProfessionalDetailsModel.objects.using('user_db').values().filter(user=UserModel(id=users_data[i]['id'])).first()
            if income_range_id is not None:
               users_data[i]['income_range_data'] = IncomeModel.objects.using('income_db').values().filter(id=income_range_id['income_range_id']).get()
               users_data[i]['designation_data'] = DesignationModel.objects.using('designation_db').values().filter(id=income_range_id['designation_id']).get()
               users_data[i]['designation_title'] = income_range_id['designation_title']
               users_data[i]['designation_data'].pop('created_at')
               users_data[i]['designation_data'].pop('updated_at')
               users_data[i]['income_range_data'].pop('created_at')
               users_data[i]['income_range_data'].pop('updated_at')
            users_data[i]['age'] = UserHealthDetailsModel.objects.using('user_db').values().filter(user=UserModel(id=users_data[i]['id'])).get()['age']
            users_data[i].pop('created_at')
            users_data[i].pop('updated_at')
        if(request_data['sortBy'] == 'Commitment done (max to min)'):
            users_data = sorted(users_data, key=lambda d: d['commitments_details']['total_commitments_done'],reverse=True)[start:end]
        elif(request_data['sortBy'] == 'Commitment done (min to max)'):
            users_data = sorted(users_data, key=lambda d: d['commitments_details']['total_commitments_done'],reverse=False)[start:end]
        elif(request_data['filterByCategory'] == "" and request_data['filterByDesignation'] == "" and request_data['sortBy'] == "" and search_param != ""):
            users_data = users_data[start:end]
        print(f"final_data length {users_data.count()}")
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
        users_data = UserModel.objects.using('user_db').values().filter(is_verified=False,is_admin=False).order_by('-joining_date').all()
        for i in range(0,len(users_data)):
            city = UserLocationDetailsModel.objects.using('user_db').values().filter(user=UserModel(id=users_data[i]['id'])).get()
            print(city)
            if city is not None:
               users_data[i]['city_data'] = CitiesModel.objects.using('location_db').values().filter(id=city['city_id']).get()
               users_data[i]['city_data'].pop('created_at')
               users_data[i]['city_data'].pop('updated_at')
            income_range_id = UserProfessionalDetailsModel.objects.using('user_db').values().filter(user=UserModel(id=users_data[i]['id'])).get()
            if income_range_id is not None:
               users_data[i]['income_range_data'] = IncomeModel.objects.using('income_db').values().filter(id=income_range_id['income_range_id']).get()
               users_data[i]['designation_data'] = DesignationModel.objects.using('designation_db').values().filter(id=income_range_id['designation_id']).get()
               users_data[i]['designation_title'] = income_range_id['designation_title']
               users_data[i]['designation_data'].pop('created_at')
               users_data[i]['designation_data'].pop('updated_at')
               users_data[i]['income_range_data'].pop('created_at')
               users_data[i]['income_range_data'].pop('updated_at')
            users_data[i]['age'] = UserHealthDetailsModel.objects.using('user_db').values().filter(user=UserModel(id=users_data[i]['id'])).get()['age']
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
        users_data = UserModel.objects.using('user_db').values().filter(is_active=True).all()
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
            print("lled")
            users_data[i]['commitments'] = []
            max_done_commitments['user_id'] = users_data[i]['id']
            commitment_data = CommitmentModel.objects.using('commitment_db').values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],is_done = True,is_updated = True).all()
            max_done_commitments['max_commitments'] = len(commitment_data)
            print("dcd")
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
        total_categories = CommitmentCategoryModel.objects.using('commitment_db').values().filter().all()
        finalData = []
        for k in range(0,len(user_ids)):
            users_data = UserModel.objects.using('user_db').values().filter(id=user_ids[k],is_active=True).all()
            for i in range(0,len(users_data)):
                commitments_data = CommitmentModel.objects.using('commitment_db').values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id']).all()
                users_data[i]['commitments_details'] = {}
                users_data[i]['commitments_details']['total_commitments'] = commitments_data.count()
                done_commitments_data = CommitmentModel.objects.using('commitment_db').values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],is_done = True,is_updated = True).all()
                users_data[i]['commitments_details']['total_commitments_done'] = done_commitments_data.count()
                notDone_commitments_data = CommitmentModel.objects.using('commitment_db').values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],is_done = False,is_updated = True).all()
                users_data[i]['commitments_details']['total_commitments_not_done'] = notDone_commitments_data.count()
                notUpdated_commitments_data = CommitmentModel.objects.using('commitment_db').values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],is_done = False,is_updated = False).all()
                users_data[i]['commitments_details']['total_commitments_not_updated'] = notUpdated_commitments_data.count()
                users_data[i]['commitments_details']['category_wise'] = []
                for j in range(0,len(total_categories)):
                    data = {}
                    commitments_data = CommitmentModel.objects.using('commitment_db').values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],category = CommitmentCategoryModel(id=total_categories[j]['id'])).all()
                    data['total_commitments'] = commitments_data.count()
                    done_commitments_data = CommitmentModel.objects.using('commitment_db').values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],category = CommitmentCategoryModel(id=total_categories[j]['id']),is_done = True,is_updated = True).all()
                    data['total_commitments_done'] = done_commitments_data.count()
                    notDone_commitments_data = CommitmentModel.objects.using('commitment_db').values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],category = CommitmentCategoryModel(id=total_categories[j]['id']),is_done = False,is_updated = True).all()
                    data['total_commitments_not_done'] = notDone_commitments_data.count()
                    notUpdated_commitments_data = CommitmentModel.objects.using('commitment_db').values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],category = CommitmentCategoryModel(id=total_categories[j]['id']),is_done = False,is_updated = False).all()
                    data['total_commitments_not_updated'] = notUpdated_commitments_data.count()
                    data['category_name'] = total_categories[j]['name']
                    users_data[i]['commitments_details']['category_wise'].append(data)
                users_data[i].pop('created_at')
                users_data[i].pop('updated_at')
                city_id = UserLocationDetailsModel.objects.using('user_db').values().filter(user=UserModel(id=users_data[i]['id'])).get()
                if city_id is not None:
                  users_data[i]['city_data'] = CitiesModel.objects.using('location_db').values().filter(id=city_id['city_id']).get()
                  users_data[i]['city_data'].pop('created_at')
                  users_data[i]['city_data'].pop('updated_at')
                  income_range_id = UserProfessionalDetailsModel.objects.using('user_db').values().filter(user=UserModel(id=users_data[i]['id'])).get()
                if income_range_id is not None:
                   users_data[i]['income_range_data'] = IncomeModel.objects.using('income_db').values().filter(id=income_range_id['income_range_id']).get()
                   users_data[i]['designation_data'] = DesignationModel.objects.using('designation_db').values().filter(id=income_range_id['designation_id']).get()
                   users_data[i]['designation_title'] = income_range_id['designation_title']
                   users_data[i]['designation_data'].pop('created_at')
                   users_data[i]['designation_data'].pop('updated_at')
                   users_data[i]['income_range_data'].pop('created_at')
                   users_data[i]['income_range_data'].pop('updated_at')
                users_data[i]['age'] = UserHealthDetailsModel.objects.using('user_db').values().filter(user=UserModel(id=users_data[i]['id'])).get()['age']
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
        all_users_data = UserModel.objects.using('user_db').values().filter(is_active=True).all()
        today = datetime.now()
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        sub_start_date = datetime.strptime(str(start).split(" ")[0], "%Y-%m-%d").date()
        sub_end_date = datetime.strptime(str(end).split(" ")[0], "%Y-%m-%d").date()
        total_categories = CommitmentCategoryModel.objects.using('commitment_db').values().filter().all()
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
                commitment_data = CommitmentModel.objects.using('commitment_db').values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id =all_users_data[i]['id'],is_done = True,is_updated = True,category = CommitmentCategoryModel(id=total_categories[index]['id'])).all()
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
                users_data = UserModel.objects.using('user_db').values().filter(id=user_ids[k],is_active=True).all()
                for i in range(0,len(users_data)):
                    commitments_data = CommitmentModel.objects.using('commitment_db').values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id']).all()
                    users_data[i]['commitments_details'] = {}
                    users_data[i]['commitments_details']['total_commitments'] = commitments_data.count()
                    done_commitments_data = CommitmentModel.objects.using('commitment_db').values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],is_done = True,is_updated = True).all()
                    users_data[i]['commitments_details']['total_commitments_done'] = done_commitments_data.count()
                    notDone_commitments_data = CommitmentModel.objects.using('commitment_db').values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],is_done = False,is_updated = True).all()
                    users_data[i]['commitments_details']['total_commitments_not_done'] = notDone_commitments_data.count()
                    notUpdated_commitments_data = CommitmentModel.objects.using('commitment_db').values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],is_done = False,is_updated = False).all()
                    users_data[i]['commitments_details']['total_commitments_not_updated'] = notUpdated_commitments_data.count()
                    users_data[i]['commitments_details']['category_wise'] = []
                    for j in range(0,len(total_categories)):
                        data = {}
                        commitments_data = CommitmentModel.objects.using('commitment_db').values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],category = CommitmentCategoryModel(id=total_categories[j]['id'])).all()
                        data['total_commitments'] = commitments_data.count()
                        done_commitments_data_category = CommitmentModel.objects.using('commitment_db').values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],category = CommitmentCategoryModel(id=total_categories[j]['id']),is_done = True,is_updated = True).all()
                        data['total_commitments_done'] = done_commitments_data_category.count()
                        notDone_commitments_data = CommitmentModel.objects.using('commitment_db').values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],category = CommitmentCategoryModel(id=total_categories[j]['id']),is_done = False,is_updated = True).all()
                        data['total_commitments_not_done'] = notDone_commitments_data.count()
                        notUpdated_commitments_data = CommitmentModel.objects.using('commitment_db').values().filter(Q(commitment_date__range=[sub_start_date, sub_end_date])).filter(user_id = users_data[i]['id'],category = CommitmentCategoryModel(id=total_categories[j]['id']),is_done = False,is_updated = False).all()
                        data['total_commitments_not_updated'] = notUpdated_commitments_data.count()
                        data['category_name'] = total_categories[j]['name']
                        users_data[i]['commitments_details']['category_wise'].append(data)
                        users_data[i]['category_name'] = total_categories[index]['name']
                users_data[i].pop('created_at')
                users_data[i].pop('updated_at')
                city_id = UserLocationDetailsModel.objects.using('user_db').values().filter(user=UserModel(id=users_data[i]['id'])).get()
                if city_id is not None:
                  users_data[i]['city_data'] = CitiesModel.objects.using('location_db').values().filter(id=city_id['city_id']).get()
                  users_data[i]['city_data'].pop('created_at')
                  users_data[i]['city_data'].pop('updated_at')
                  income_range_id = UserProfessionalDetailsModel.objects.using('user_db').values().filter(user=UserModel(id=users_data[i]['id'])).get()
                if income_range_id is not None:
                   users_data[i]['income_range_data'] = IncomeModel.objects.using('income_db').values().filter(id=income_range_id['income_range_id']).get()
                   users_data[i]['designation_data'] = DesignationModel.objects.using('designation_db').values().filter(id=income_range_id['designation_id']).get()
                   users_data[i]['designation_title'] = income_range_id['designation_title']
                   users_data[i]['designation_data'].pop('created_at')
                   users_data[i]['designation_data'].pop('updated_at')
                   users_data[i]['income_range_data'].pop('created_at')
                   users_data[i]['income_range_data'].pop('updated_at')
                users_data[i]['age'] = UserHealthDetailsModel.objects.using('user_db').values().filter(user=UserModel(id=users_data[i]['id'])).get()['age']
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
        serializer = UserSignUpSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["id"]
            first_name = serializer.data["first_name"]
            last_name = serializer.data["last_name"]
            mobile_number = serializer.data["mobile_number"]
            password = serializer.data["password"]
            age = serializer.data["age"]
            city = serializer.data['city']
            income_range = serializer.data['income_range']
            designation_title = serializer.data["designation_title"]
            designation = serializer.data["designation"]
            is_medicine_ongoing = serializer.data["is_medicine_ongoing"]
            any_health_issues = serializer.data["any_health_issues"]
            is_subscribed = serializer.data["is_subscribed"]
            userdata = UserModel.objects.using('user_db').filter(
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
            userdata.first_name=first_name
            userdata.last_name=last_name
            userdata.mobile_number = mobile_number
            userdata.password = password
            userdata.age = age
            userdata.designation_title = designation_title
            # userdata.designation = DesignationModel(id=designation)
            # userdata.city = CitiesModel(id=city)
            userdata.is_medicine_ongoing = is_medicine_ongoing
            userdata.any_health_issues = any_health_issues
            userdata.is_subscribed = is_subscribed
            # if 'income_range' in data and 'profile_pic' in request.FILES:
            #    userdata.profile_pic = f"static/{request.FILES['profile_pic']}"
            #    userdata.income_range = IncomeModel(id=income_range)
            # elif('income_range' in data and 'profile_pic' not in request.FILES):
                # userdata.income_range = IncomeModel(id=income_range)
            userdata.save()
            updated_date = list(
                UserModel.objects.using('user_db').values().filter(
                    id=user_id)
            )
            return Response(
                ResponseData.success(
                    updated_date[0]['id'], "User profile updated successfully"),
                status=status.HTTP_201_CREATED,
            )
        return Response(
            ResponseData.error(serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )
    except KeyError as exception:
        return Response(
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
            user = UserModel.objects.using('user_db').filter(
                id=user_id,is_active=True).first()
            if not user:
                return Response(
                    ResponseData.error(
                        "User id is invalid"),
                    status=status.HTTP_201_CREATED,
                )
            user_details = UserModel.objects.using('user_db').values().filter(id=user_id,is_active=True).all()
            for i in range(0,len(user_details)):
               user_details[i].pop('created_at')
               user_details[i].pop('updated_at')
               user_details[i].pop('is_active')
               city_id = UserLocationDetailsModel.objects.using('user_db').values().filter(user=UserModel(id=user_details[i]['id'])).get()
               if city_id is not None:
                user_details[i]['city_data'] = CitiesModel.objects.using('location_db').values().filter(id=city_id['city_id']).get()
                user_details[i]['city_data'].pop('created_at')
                user_details[i]['city_data'].pop('updated_at')
               income_range_id = UserProfessionalDetailsModel.objects.using('user_db').values().filter(user=UserModel(id=user_details[i]['id'])).get()
               print(income_range_id)
               if income_range_id is not None:
                user_details[i]['income_range_data'] = IncomeModel.objects.using('income_db').values().filter(id=income_range_id['income_range_id']).get()
                user_details[i]['income_range_data'].pop('created_at')
                user_details[i]['income_range_data'].pop('updated_at')
               check_data = RedeemPointsModel.objects.using('redeemPoints_db').values().filter().all()
               for j in range(0,check_data.count()):
                  if(check_data[j]['to_user_id'] == user_id and check_data[j]['is_active']):
                   user_details[i]['redeem_point_data'] = check_data[j]
                   user_details[i]['redeem_point_data'].pop('updated_at')
                   user_details[i]['redeem_point_data'].pop('created_at')
                   user_details[i]['redeem_point_data'].pop('from_user_ids')
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
def makeUserAdmin(request):
    """Function to make a user admin"""
    try:
        data = request.data
        serializer = GetUserProfileSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["id"]
            user = UserModel.objects.using('user_db').filter(
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
        is_id_valid = UserModel.objects.using('user_db').filter(id=user_id).first()
        CommitmentModel.objects.using('commitment_db').filter(user_id=user_id).delete()
        if not is_id_valid:
               return Response(
                   ResponseData.error("User id is invalid"),
                   status=status.HTTP_200_OK,
               )
        UserSubscriptionDetailsModel.objects.using('user_db').filter(user_id=user_id).delete()
        UserPaymentDetailsModel.objects.using('user_db').filter(user_id=user_id).delete()
        UserGoogleSignInModel.objects.using('user_db').filter(user_id=user_id).delete()
        UserLocationDetailsModel.objects.using('user_db').filter(user_id=user_id).delete()
        UserProfessionalDetailsModel.objects.using('user_db').filter(user_id=user_id).delete()
        UserHealthDetailsModel.objects.using('user_db').filter(user_id=user_id).delete()
        RedeemPointsModel.objects.using('redeemPoints_db').filter(from_user_id=user_id).delete()
        ReferralCodeModel.objects.using('referralCode_db').filter(user_id=user_id).delete()
        UserModel.objects.using('user_db').filter(id=user_id).delete()
        return Response(
            ResponseData.success_without_data("User details deleted successfully"),
            status=status.HTTP_201_CREATED)
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )