import hashlib
from datetime import date, datetime, timedelta
from random import randint

from django.core.files.storage import FileSystemStorage
from django.db.models import Q, Sum
from django.http.response import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from challenges_result.models import ChallengesResultModel
from commdem_warriors_backend.authenticators import ApiKeyAuthentication
from commitment.models import (
    CommitmentCategoryModel,
    CommitmentModel,
    CommitmentNameModel,
)
from designation.models import DesignationModel
from group_challenges.models import (
    GroupChallengeModel,
    GroupChallengesPaymentModel,
    GroupChallengeTypeModel,
    ParticipantsInGroupChallengesModel,
)
from income.models import IncomeModel
from location.models import (
    CitiesModel,
    CountriesDialCodeModel,
    CountriesModel,
    StatesModel,
)
from logs.models import LogsOfPagesOfUserModel
from notifications.models import UserPlayerIdModel
from questions_before_relationship.models import QuestionsToAskBeforeModel
from redeemPoints.models import RedeemPointsModel
from referralCode.models import ReferralCodeModel
from response import Response as ResponseData
from reviews.models import ReviewModel
from subscription.models import SubscriptionModel
from user.models import (
    UserAnswerBeforeRelationshipModel,
    UserFreeTrialPeriodModel,
    UserGoogleSignInModel,
    UserHealthDetailsModel,
    UserLocationDetailsModel,
    UserModel,
    UserPaymentDetailsModel,
    UserPrivacyModel,
    UserProfessionalDetailsModel,
    UserReviewModel,
    UserSubscriptionDetailsModel,
    UserWisePrivacyModel,
)
from user.serializers import (
    AddAnswersOfQuestionsBeforeRelationshipSerializer,
    AddNewPaymentSerializer,
    AddUserReviewSerializer,
    AddUserSubscriptionSerializer,
    GetReviewsOfAllUsersSerializer,
    GetUserProfileSerializer,
    GetUserSubscriptionSerializer,
    UpdateUserPrivacySerializer,
    UpdateUserReviewSerializer,
    UserSignUpSerializer,
    UserSubscribedOrNotSerializer,
)
from voiceAssistant.models import (
    userPreferredVoiceLanguageModel,
    voiceAssistantLanguagesModel,
)
from warriors_workout_videos.models import WarriorsWorkoutVideosModel


def terms_and_conditions(request):
    # Fetch the content of terms and conditions

    return render(request, "terms_and_conditions.html")


def privacy_policy(request):
    # Fetch the privacy policy of our app

    return render(request, "privacy_policy.html")


def dashboard(request):
    # Fetch dashboard of our app

    return render(request, "dashboard.html")


load_dotenv()


def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10**n) - 1
    return randint(range_start, range_end)


# Create your views here.
@api_view(["POST"])
def signup(request):
    """Function to add new user"""
    try:
        data = request.data
        serializer = UserSignUpSerializer(data=data)
        print(data)
        if serializer.is_valid():
            full_name = serializer.data["full_name"]
            mobile_number = serializer.data["mobile_number"]
            password = serializer.data["password"]
            email = serializer.data["email"]
            virtual_assistant_language_id = serializer.data[
                "virtual_assistant_language_id"
            ]
            birth_date = serializer.data["birth_date"]
            profile_pic = (
                request.FILES["profile_pic"] if "profile_pic" in request.FILES else ""
            )
            referred_user_phone_number = (
                serializer.data["referred_user_phone_number"]
                if "referred_user_phone_number" in data
                else ""
            )
            referred_user_full_name = (
                serializer.data["referred_user_full_name"]
                if "referred_user_full_name" in data
                else ""
            )
            gender = serializer.data["gender"]
            weight = serializer.data["weight"]
            height = serializer.data["height"]
            age = serializer.data["age"]
            designation_title = serializer.data["designation_title"]
            designation = serializer.data["designation"]
            city_id = serializer.data["city_id"]
            state_id = serializer.data["state_id"]
            country_id = serializer.data["country_id"]
            # income_range = serializer.data['income_range']
            is_medicine_ongoing = serializer.data["is_medicine_ongoing"]
            any_health_issues = serializer.data["any_health_issues"]
            player_id = (
                serializer.data["player_id"] if "player_id" in request.data else ""
            )
            serializer.data["user_uid"] if "user_uid" in request.data else ""
            (
                serializer.data["user_gmail_id"]
                if "user_gmail_id" in request.data
                else ""
            )
            user = UserModel.objects.filter(
                Q(email__icontains=email) | Q(mobile_number__icontains=mobile_number)
            ).first()
            if user:
                return Response(
                    ResponseData.error("User is already registered please log in"),
                    status=status.HTTP_201_CREATED,
                )
            data = f"{mobile_number}_{datetime.now()}"
            if profile_pic != "":
                fs = FileSystemStorage(location="static/")
                fs.save(profile_pic.name, profile_pic)
            new_user = UserModel.objects.create(
                full_name=full_name,
                mobile_number=mobile_number,
                email=email,
                profile_pic="" if profile_pic == "" else f"static/{profile_pic}",
                password=password,
                rank=len(UserModel.objects.filter(is_active=True).all()) + 1,
                birth_date=birth_date,
                is_verified=True if mobile_number == "+917020829599" else False,
                is_admin=True if mobile_number == "+917020829599" else False,
                is_active=True if mobile_number == "+917020829599" else False,
                api_key=hashlib.sha256(data.encode()).hexdigest(),
            )
            new_user.save()
            if referred_user_phone_number != "":
                new_referral_data = ReferralCodeModel.objects.create(
                    user_id=new_user.id,
                    referred_user_phone_number=referred_user_phone_number,
                    referred_user_full_name=referred_user_full_name,
                )
                new_referral_data.save()
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
                city_name=city_name.name,
            )
            new_user_location.save()
            new_user_professional_details = UserProfessionalDetailsModel.objects.create(
                designation_title=designation_title,
                user=UserModel(id=new_user.id),
                designation_id=designation,
                # income_range_id=income_range,
            )
            new_user_professional_details.save()
            current_date = datetime.now().date()
            ninth_of_month = date(current_date.year, current_date.month, 9)
            if current_date > ninth_of_month:
                next_month = current_date.replace(day=1) + timedelta(days=30)
                next_month_10th = date(next_month.year, next_month.month, 10)
                datetime.combine(next_month_10th, datetime.min.time())
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
                    voice_assistant_language=voiceAssistantLanguagesModel(
                        id=virtual_assistant_language_id
                    ),
                )
                user_language_data.save()
            generated_referral_code = random_with_N_digits(6)
            if "player_id" != "":
                store_player_id = UserPlayerIdModel.objects.create(
                    user_id=new_user.id,
                    player_id=player_id,
                )
                store_player_id.save()
            list_of_player_ids = []
            all_admin_users = UserModel.objects.filter(
                is_admin=True, is_active=True
            ).all()
            for i in range(0, all_admin_users.count()):
                admin_player_id = UserPlayerIdModel.objects.filter(
                    user_id=all_admin_users[i].id, is_active=True
                ).all()
                for j in range(0, admin_player_id.count()):
                    list_of_player_ids.append(admin_player_id[j].player_id)
            print(list_of_player_ids)
            # data = {
            #      "app_id": os.getenv('ONESIGNAL_APP_ID'),
            #      "include_player_ids" : list_of_player_ids,
            #      "data": {"foo": f"New user joined recently"},
            #      "contents": {"en": "Please check if profile is valid or not"}}
            # R.post(f"{os.getenv('BASE_URL')}/notifications",json=data)
            free_trial_start_date = datetime.now().date()
            free_trial_end_date = free_trial_start_date
            if 10 <= free_trial_start_date.day <= 31:
                next_month = free_trial_start_date.replace(day=1) + timedelta(days=32)
                free_trial_end_date = free_trial_start_date + timedelta(
                    days=61 - free_trial_start_date.day
                )
            else:
                next_month = free_trial_start_date.replace(day=1) + timedelta(days=11)
                free_trial_end_date = free_trial_start_date.replace(
                    day=free_trial_start_date.day + 30
                )
            user_free_trial_period = UserFreeTrialPeriodModel.objects.create(
                user=UserModel(id=new_user.id),
                start_date=free_trial_start_date,
                end_date=free_trial_end_date,
            )
            user_free_trial_period.save()
            next_10th_date = next_month.replace(day=10)
            next_20th_date = next_month.replace(day=20)
            print(f"next_10th_date {next_10th_date}")
            print(f"next_20th_date {next_20th_date}")
            query = Q(challenge_date=next_10th_date) | Q(challenge_date=next_20th_date)
            challenge_type_data = GroupChallengeTypeModel.objects.filter(
                type="free_trial"
            ).last()
            matching_records = GroupChallengeModel.objects.filter(
                query, is_active=True, challenge_type__type="free_trial"
            ).values_list("id", flat=True)
            for i in range(0, len(list(matching_records))):
                make_user_participant = (
                    ParticipantsInGroupChallengesModel.objects.create(
                        user_id=new_user.id,
                        challenge_type_id=challenge_type_data.id,
                        group_challenge_id=list(matching_records)[i],
                    )
                )
                make_user_participant.save()
            return Response(
                ResponseData.success_for_referral_code(
                    "Please give sometime to verify your account",
                    generated_referral_code,
                ),
                status=status.HTTP_201_CREATED,
            )
        for error in serializer.errors:
            print(serializer.errors[error][0])
        return Response(
            ResponseData.error(serializer.errors[error][0]),
            status=status.HTTP_201_CREATED,
        )
    except Exception as exception:
        print(f"str(exception) {str(exception)}")
        return Response(
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
# @authentication_classes([ApiKeyAuthentication])  # Apply API key authentication
def signin(request):
    """Function to let user sign in"""
    try:
        data = request.data
        print(f"data {data}")
        if "uid" in request.data:
            google_data = UserGoogleSignInModel.objects.filter(
                uid=data["uid"], is_active=True
            ).first()
            if not google_data:
                return Response(
                    ResponseData.error(
                        "Google account does not exists, please register first"
                    ),
                    status=status.HTTP_201_CREATED,
                )
            user_data = UserModel.objects.filter(
                id=google_data.user_id, is_active=True
            ).first()
            country_details = UserLocationDetailsModel.objects.filter(
                user_id=google_data.user_id, is_active=True
            ).first()
            country_code = CountriesModel.objects.filter(
                country_id=country_details.country_id
            ).first()
            country_dial_code = CountriesDialCodeModel.objects.filter(
                country_code=country_code.country_code
            ).first()
            data["mobile_number"] = str(user_data.mobile_number)
        user = UserModel.objects.filter(
            Q(mobile_number__icontains=data["mobile_number"])
        ).first()
        if not user:
            return Response(
                ResponseData.error("Account does not exists, please register first"),
                status=status.HTTP_201_CREATED,
            )
        print(request.data)
        country_details = UserLocationDetailsModel.objects.filter(
            user=UserModel(id=user.id, is_active=True)
        ).first()
        country_code = CountriesModel.objects.filter(
            country_id=country_details.country_id
        ).first()
        country_dial_code = CountriesDialCodeModel.objects.filter(
            country_code=country_code.country_code
        ).first()
        data["mobile_number"] = country_dial_code.country_dial_code + str(
            user.mobile_number
        )
        playerId = data["player_id"]
        if user.mobile_number != "+917020829599":
            if not user.is_verified:
                return Response(
                    ResponseData.error("Please wait while admin verifies your account"),
                    status=status.HTTP_201_CREATED,
                )
        user_details = (
            UserModel.objects.values().filter(id=user.id, is_active=True).all()
        )
        referral_code = ReferralCodeModel.objects.filter(
            user_id=user_details[0]["id"]
        ).first()
        for i in range(0, len(user_details)):
            if referral_code is not None:
                user_details[i][
                    "referred_user_mobile_number"
                ] = referral_code.referred_user_phone_number
                user_details[i][
                    "referred_user_full_name"
                ] = referral_code.referred_user_full_name
            user_details[i].pop("created_at")
            user_details[i].pop("updated_at")
        player_id_exists = UserPlayerIdModel.objects.filter(
            user_id=user_details[0]["id"], player_id=playerId
        ).first()
        if player_id_exists:
            player_id_exists.player_id = playerId
            player_id_exists.save()
        else:
            store_player_id = UserPlayerIdModel.objects.create(
                user_id=user_details[0]["id"],
                player_id=playerId,
            )
            store_player_id.save()
        does_today_data_exists = LogsOfPagesOfUserModel.objects.filter(
            user_id=user.id
        ).last()
        if does_today_data_exists is None:
            new_data = LogsOfPagesOfUserModel.objects.create(
                user_id=user.id, otp_page=1
            )
            new_data.save()
        else:
            does_today_data_exists.otp_page = does_today_data_exists.otp_page + 1
            does_today_data_exists.save()
        print("vsvvdvdss")
        return Response(
            ResponseData.success(user_details, "User logged in successfully"),
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
            user_id = serializer.data["id"]
            user = UserModel.objects.filter(id=user_id, is_active=True).first()
            if not user:
                return Response(
                    ResponseData.error(
                        "Account does not exists, please register first"
                    ),
                    status=status.HTTP_201_CREATED,
                )
            free_trial_data = UserFreeTrialPeriodModel.objects.filter(
                user_id=user_id, is_active=True
            ).last()
            if free_trial_data is not None:
                current_date = datetime.now().date()
                print(f"current_date {current_date}")
                if current_date > free_trial_data.end_date:
                    free_trial_data.is_active = False
                    free_trial_data.save()
                    return Response(
                        ResponseData.common_subscription_message(
                            "Free trial is over", False, False
                        ),
                        status=status.HTTP_201_CREATED,
                    )
                return Response(
                    ResponseData.common_subscription_message(
                        "Free trial is active", True, False
                    ),
                    status=status.HTTP_201_CREATED,
                )
            user_subscription_details = UserPaymentDetailsModel.objects.filter(
                user=UserModel(id=user_id), is_active=True
            ).last()
            if user_subscription_details is None:
                return Response(
                    ResponseData.common_subscription_message(
                        "You are not subscribed currently", False, False
                    ),
                    status=status.HTTP_201_CREATED,
                )
            current_date = timezone.now().date()
            if current_date > user_subscription_details.subscription_end_date:
                user_subscription_details.is_active = False
                user_subscription_details.save()
                user.is_subscribed = False
                user.save()
                return JsonResponse(
                    ResponseData.common_subscription_message(
                        "Your subscription is over", False, False
                    ),
                )
            else:
                return JsonResponse(
                    ResponseData.common_subscription_message(
                        "You are subscribed", False, True
                    ),
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

        return getattr(self, "case_" + str(month), lambda: default)()

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
@authentication_classes(
    [
        ApiKeyAuthentication,
    ]
)
def addNewPayment(request):
    """Function to add new payment done by a user"""
    try:
        data = request.data
        print(data)
        serializer = AddNewPaymentSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            challenge_type = serializer.data["challenge_type"]
            payment_id = serializer.data["payment_id"]
            subscription_id = serializer.data["subscription_id"]
            group_challenge_id = serializer.data["group_challenge_id"]
            date_of_payment = str(serializer.data["date_of_payment"]).split(" ")[0]
            challenge_type_data = GroupChallengeTypeModel.objects.filter(
                type=challenge_type
            ).last()
            total_participants_already = (
                ParticipantsInGroupChallengesModel.objects.filter(
                    group_challenge_id=group_challenge_id,
                ).count()
            )
            if subscription_id != 0:
                subscription_details = SubscriptionModel.objects.filter(
                    id=subscription_id
                ).first()
                if subscription_details is None:
                    return Response(
                        ResponseData.error("Subscription id is invalid"),
                        status=status.HTTP_200_OK,
                    )
                last_date_of_subscription = datetime.strptime(
                    date_of_payment, "%Y-%m-%d"
                ) + timedelta(days=int(subscription_details.duration))
                new_payment_record = UserPaymentDetailsModel.objects.create(
                    user_id=user_id,
                    payment_id=payment_id,
                    subscription_id=subscription_id,
                    date_of_payment=date_of_payment,
                    subscription_end_date=last_date_of_subscription,
                    is_active=True,
                )
                new_payment_record.save()
                free_trial_data = UserFreeTrialPeriodModel.objects.filter(
                    user_id=user_id, is_active=True
                ).last()
                if free_trial_data is not None:
                    free_trial_data.is_active = False
                    free_trial_data.save()
                    todays_date = datetime.now().date()
                    get_future_free_trial_participant_data = (
                        ParticipantsInGroupChallengesModel.objects.filter(
                            challenge_type__type=challenge_type,
                            user_id=user_id,
                            date_of_submission__gte=todays_date,
                            has_submitted_video=False,
                        )
                    )
                    for record in get_future_free_trial_participant_data:
                        record.is_active = False
                        record.save()
                user_data = UserModel.objects.filter(id=user_id, is_active=True).first()
                user_data.is_subscribed = True
                user_data.save()
                # Get the current date
                current_date = datetime.now().date()

                # Calculate the upcoming 15th and 25th dates
                if current_date.day <= 15:
                    next_15th_date = datetime(current_date.year, current_date.month, 15)
                else:
                    next_month = current_date.replace(day=1) + timedelta(days=32)
                    next_15th_date = datetime(next_month.year, next_month.month, 15)

                if current_date.day <= 25:
                    next_25th_date = datetime(current_date.year, current_date.month, 25)
                else:
                    next_month = current_date.replace(day=1) + timedelta(days=32)
                    next_25th_date = datetime(next_month.year, next_month.month, 25)

                # Print the upcoming dates for reference
                print(f"Today's Date: {current_date}")
                print(f"Upcoming 15th Date: {next_15th_date.date()}")
                print(f"Upcoming 25th Date: {next_25th_date.date()}")

                # Create records in ParticipantsInGroupChallengesForFreeTrialModel for the upcoming challenge dates  # noqa: E501
                query = Q(challenge_date=next_15th_date) | Q(
                    challenge_date=next_25th_date
                )
                matching_records = GroupChallengeModel.objects.filter(
                    query,
                    challenge_type__type=challenge_type,
                    is_active=True,
                    subscription_id=subscription_id,
                ).values_list("id", flat=True)
                print(f"matching_records {matching_records}")
                for record_id in matching_records:
                    make_user_participant = (
                        ParticipantsInGroupChallengesModel.objects.create(
                            user_id=user_id,
                            challenge_type=GroupChallengeTypeModel.objects.get(type=challenge_type),
                            group_challenge_id=record_id,
                        )
                    )
                    make_user_participant.save()
                return Response(
                    ResponseData.success_without_data(
                        "Subscription purchased successfully"
                    ),
                    status=status.HTTP_201_CREATED,
                )
            elif (
                challenge_type != "custom_private_bidding"
                and challenge_type != "custom_public_bidding"
            ):
                group_challenge_details = GroupChallengeModel.objects.get(
                    id=group_challenge_id,
                )
                if (
                    int(group_challenge_details.max_participants_allowed)
                    == total_participants_already
                ):
                    group_challenge_details.max_participants_allowed = str(
                        int(group_challenge_details.max_participants_allowed) + 1
                    )
                    print(group_challenge_details.max_participants_allowed)
                    group_challenge_details.save()
                biddingChallengeDetails = GroupChallengesPaymentModel.objects.filter(
                    user_id=user_id,
                    challenge_type_id=challenge_type_data.id,
                    group_challenge=GroupChallengeModel(id=group_challenge_id),
                ).first()
                if biddingChallengeDetails is not None:
                    return Response(
                        ResponseData.error(
                            "You have already made payment for this challenge"
                        ),
                        status=status.HTTP_200_OK,
                    )
                new_payment_record = GroupChallengesPaymentModel.objects.create(
                    user_id=user_id,
                    challenge_type_id=challenge_type_data.id,
                    payment_id=payment_id,
                    group_challenge=GroupChallengeModel(id=group_challenge_id),
                    date_of_payment=date_of_payment,
                )
                new_payment_record.save()
                new_data = ParticipantsInGroupChallengesModel.objects.create(
                    user_id=user_id,
                    challenge_type_id=challenge_type_data.id,
                    group_challenge_id=group_challenge_id,
                )
                new_data.save()
                return Response(
                    ResponseData.success_without_data(
                        "You are added in this challenge successfully"
                    ),
                    status=status.HTTP_201_CREATED,
                )
            elif challenge_type == "custom_public_bidding":
                if (
                    int(group_challenge_details.max_participants_allowed)
                    == total_participants_already
                ):
                    group_challenge_details.max_participants_allowed = str(
                        int(group_challenge_details.max_participants_allowed) + 1
                    )
                    print(group_challenge_details.max_participants_allowed)
                    group_challenge_details.save()
                biddingChallengeDetails = GroupChallengesPaymentModel.objects.filter(
                    user_id=user_id,
                    challenge_type_id=challenge_type_data.id,
                    group_challenge=GroupChallengeModel(id=group_challenge_id),
                ).first()
                if biddingChallengeDetails is not None:
                    return Response(
                        ResponseData.error(
                            "You have already made payment for this challenge"
                        ),
                        status=status.HTTP_200_OK,
                    )
                new_payment_record = GroupChallengesPaymentModel.objects.create(
                    user_id=user_id,
                    payment_id=payment_id,
                    challenge_type_id=challenge_type_data.id,
                    group_challenge=GroupChallengeModel(id=group_challenge_id),
                    date_of_payment=date_of_payment,
                )
                new_payment_record.save()
                new_data = ParticipantsInGroupChallengesModel.objects.create(
                    user_id=user_id,
                    challenge_type_id=challenge_type_data.id,
                    group_challenge_id=group_challenge_id,
                )
                new_data.save()
                return Response(
                    ResponseData.success_without_data(
                        "You are added in this challenge successfully"
                    ),
                    status=status.HTTP_201_CREATED,
                )
            elif challenge_type == "custom_private_bidding":
                new_payment_record = GroupChallengesPaymentModel.objects.create(
                    user_id=user_id,
                    challenge_type_id=challenge_type_data.id,
                    payment_id=payment_id,
                    group_challenge=GroupChallengeModel(id=group_challenge_id),
                    date_of_payment=date_of_payment,
                )
                new_payment_record.save()
                return Response(
                    ResponseData.success_without_data("Payment done successfully"),
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
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@authentication_classes(
    [
        ApiKeyAuthentication,
    ]
)
def addNewSubscription(request):
    """Function to add new subscription details of a user"""
    try:
        data = request.data
        serializer = AddUserSubscriptionSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            subscription_id = serializer.data["subscription_id"]
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response(
                    ResponseData.error("User id is invalid"),
                    status=status.HTTP_201_CREATED,
                )
            subscription = SubscriptionModel.objects.filter(id=subscription_id).first()
            if not subscription:
                return Response(
                    ResponseData.error("Subscription id is invalid"),
                    status=status.HTTP_201_CREATED,
                )
            does_subscription_exists = UserSubscriptionDetailsModel.objects.filter(
                user_id=user_id, is_active=True
            ).first()
            if does_subscription_exists:
                return Response(
                    ResponseData.error("You are already subscribed currently"),
                    status=status.HTTP_201_CREATED,
                )
            new_subscription = UserSubscriptionDetailsModel.objects.create(
                user=UserModel(id=user_id),
                subscription_id=subscription_id,
                is_active=True,
            )
            new_subscription.save()
            return Response(
                ResponseData.success_without_data("Subscription done successfully"),
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
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@authentication_classes(
    [
        ApiKeyAuthentication,
    ]
)
def getUserSubscriptionById(request):
    """Function to get subscription based on user id"""
    try:
        data = request.data
        serializer = GetUserSubscriptionSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user"]
            subscription_id = serializer.data["subscription"]
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response(
                    ResponseData.error("User id is invalid"),
                    status=status.HTTP_201_CREATED,
                )
            subscription = SubscriptionModel.objects.filter(id=subscription_id).first()
            if not subscription:
                return Response(
                    ResponseData.error("Subscription id is invalid"),
                    status=status.HTTP_201_CREATED,
                )
            subscription_data = (
                UserSubscriptionDetailsModel.objects.values()
                .filter(id=subscription_id, user=UserModel(id=user_id))
                .all()
            )
            for i in range(0, subscription_data.count()):
                subscription_data[i].pop("created_at")
                subscription_data[i].pop("updated_at")
            return Response(
                ResponseData.success(
                    subscription_data, "Subscription fetched successfully"
                ),
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
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@authentication_classes(
    [
        ApiKeyAuthentication,
    ]
)
def getAllSubscriptionsOfUser(request):
    """Function to get all subscriptions of a user"""
    try:
        data = request.data
        serializer = GetUserSubscriptionSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user"]
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response(
                    ResponseData.error("User id is invalid"),
                    status=status.HTTP_201_CREATED,
                )
            subscription_data = (
                UserSubscriptionDetailsModel.objects.values()
                .filter(user=UserModel(id=user_id), is_active=True)
                .all()
            )
            for i in range(0, subscription_data.count()):
                subscription_data[i].pop("created_at")
                subscription_data[i].pop("updated_at")
            return Response(
                ResponseData.success(
                    subscription_data, "Subscriptions fetched successfully"
                ),
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
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@authentication_classes(
    [
        ApiKeyAuthentication,
    ]
)
def getAllUsersDetails(request):
    """Function to get details of all users"""
    try:
        request_data = request.data
        print(request_data)
        user_id = request.data["user_id"]
        page_number = int(request_data["page_no"])
        page_size_param = int(request_data["page_size"])
        search_param = (
            request_data["search_param"] if "search_param" in request.data else ""
        )
        my_matches_ids = (
            request_data["my_matches_ids"] if "my_matches_ids" in request.data else ""
        )
        challenge_id = (
            request_data["challenge_id"] if "challenge_id" in request.data else 0
        )
        page_no = page_number
        page_size = page_size_param
        start = (page_no - 1) * page_size
        end = page_no * page_size
        print(f"request_data {request_data}")
        user_ids_list = request_data["all_participants_id"]
        filter_condition = Q(is_active=True)
        if user_ids_list:
            filter_condition &= Q(id__in=user_ids_list)
        get_all_users = (
            UserModel.objects.values().filter(filter_condition).order_by("rank").all()
        )
        for i in range(0, len(get_all_users)):
            is_relation_there = UserWisePrivacyModel.objects.filter(
                my_details_id=user_id, other_user_details_id=get_all_users[i]["id"]
            ).first()
            if is_relation_there is None:
                new_relation_data = UserWisePrivacyModel.objects.create(
                    my_details_id=user_id,
                    other_user_details_id=get_all_users[i]["id"],
                )
                new_relation_data.save()
        if my_matches_ids != "":
            print("dfvdfvfdvdfvdf")
            users_data = UserModel.objects.values().filter(id__in=my_matches_ids).all()
        else:
            if (
                request_data["filterByCategory"] == ""
                and request_data["filterByDesignation"] == ""
                and request_data["sortBy"] == ""
                and search_param == ""
            ):
                print("123")
                users_data = (
                    UserModel.objects.values()
                    .filter(filter_condition)
                    .order_by("rank")
                    .all()[start:end]
                )
                print(len(users_data))
            elif (
                request_data["sortBy"] == "Age (max to min)"
                and request_data["filterByDesignation"] == ""
            ):
                users_data = (
                    UserModel.objects.values()
                    .filter(filter_condition)
                    .order_by("-userhealthdetailsmodel__age")
                    .all()[start:end]
                    if search_param == ""
                    else UserModel.objects.values()
                    .filter(
                        Q(full_name__icontains=search_param)
                        | Q(mobile_number__icontains=search_param)
                        | Q(
                            userlocationdetailsmodel__city_name__icontains=search_param
                        ),
                        filter_condition,
                    )
                    .order_by("-userhealthdetailsmodel__age")
                    .all()[start:end]
                )
            elif (
                request_data["sortBy"] == "Age (min to max)"
                and request_data["filterByDesignation"] == ""
            ):
                users_data = (
                    UserModel.objects.values()
                    .filter(filter_condition)
                    .order_by("userhealthdetailsmodel__age")
                    .all()[start:end]
                    if search_param == ""
                    else UserModel.objects.values()
                    .filter(
                        Q(full_name__icontains=search_param)
                        | Q(mobile_number__icontains=search_param)
                        | Q(
                            userlocationdetailsmodel__city_name__icontains=search_param
                        ),
                        filter_condition,
                    )
                    .order_by("userhealthdetailsmodel__age")
                    .all()[start:end]
                )
            elif (
                request_data["sortBy"] == "Rank"
                and request_data["filterByDesignation"] == ""
            ):
                users_data = (
                    UserModel.objects.values()
                    .filter(filter_condition)
                    .order_by("-rank")
                    .all()[start:end]
                    if search_param == ""
                    else UserModel.objects.values()
                    .filter(
                        Q(full_name__icontains=search_param)
                        | Q(mobile_number__icontains=search_param)
                        | Q(
                            userlocationdetailsmodel__city_name__icontains=search_param
                        ),
                        filter_condition,
                    )
                    .order_by("-rank")
                    .all()[start:end]
                )
            elif (
                request_data["sortBy"] == "Age (max to min)"
                and request_data["filterByDesignation"] != ""
            ):
                users_data = (
                    UserModel.objects.values()
                    .filter(
                        userprofessionaldetailsmodel__designation_id=request_data[
                            "filterByDesignation"
                        ],
                        is_active=True,
                    )
                    .order_by("-userhealthdetailsmodel__age")
                    .all()[start:end]
                    if search_param == ""
                    else UserModel.objects.values()
                    .filter(
                        Q(full_name__icontains=search_param)
                        | Q(mobile_number__icontains=search_param)
                        | Q(
                            userlocationdetailsmodel__city__name__icontains=search_param
                        ),
                        filter_condition,
                    )
                    .filter(
                        userprofessionaldetailsmodel__designation_id=request_data[
                            "filterByDesignation"
                        ]
                    )
                    .order_by("-userhealthdetailsmodel__age")
                    .all()[start:end]
                )
            elif (
                request_data["sortBy"] == "Age (min to max)"
                and request_data["filterByDesignation"] != ""
            ):
                users_data = (
                    UserModel.objects.values()
                    .filter(
                        userprofessionaldetailsmodel__designation_id=request_data[
                            "filterByDesignation"
                        ],
                        is_active=True,
                    )
                    .order_by("userhealthdetailsmodel__age")
                    .all()[start:end]
                    if search_param == ""
                    else UserModel.objects.values()
                    .filter(
                        Q(full_name__icontains=search_param)
                        | Q(mobile_number__icontains=search_param)
                        | Q(
                            userlocationdetailsmodel__city__name__icontains=search_param
                        ),
                        filter_condition,
                    )
                    .filter(
                        userprofessionaldetailsmodel__designation_id=request_data[
                            "filterByDesignation"
                        ]
                    )
                    .order_by("userhealthdetailsmodel__age")
                    .all()[start:end]
                )
            elif (
                request_data["sortBy"] == "Rank"
                and request_data["filterByDesignation"] != ""
            ):
                users_data = (
                    UserModel.objects.values()
                    .filter(
                        userprofessionaldetailsmodel__designation_id=request_data[
                            "filterByDesignation"
                        ],
                        is_active=True,
                    )
                    .order_by("-rank")
                    .all()[start:end]
                    if search_param == ""
                    else UserModel.objects.values()
                    .filter(
                        Q(full_name__icontains=search_param)
                        | Q(mobile_number__icontains=search_param)
                        | Q(
                            userlocationdetailsmodel__city__name__icontains=search_param
                        ),
                        filter_condition,
                    )
                    .filter(
                        userprofessionaldetailsmodel__designation_id=request_data[
                            "filterByDesignation"
                        ]
                    )
                    .order_by("-rank")
                    .all()[start:end]
                )
            elif request_data["filterByDesignation"] != "":
                users_data = (
                    UserModel.objects.values()
                    .filter(
                        userprofessionaldetailsmodel__designation_id=request_data[
                            "filterByDesignation"
                        ],
                        is_active=True,
                    )
                    .all()[start:end]
                    if search_param == ""
                    else UserModel.objects.values()
                    .filter(
                        Q(full_name__icontains=search_param)
                        | Q(mobile_number__icontains=search_param)
                        | Q(
                            userlocationdetailsmodel__city__name__icontains=search_param
                        ),
                        filter_condition,
                    )
                    .filter(
                        userprofessionaldetailsmodel__designation_id=request_data[
                            "filterByDesignation"
                        ]
                    )
                    .all()[start:end]
                )
            else:
                print("calledhere")
                users_data = (
                    UserModel.objects.values()
                    .filter(filter_condition)
                    .order_by("rank")
                    .all()
                    if search_param == ""
                    else UserModel.objects.values()
                    .filter(
                        Q(full_name__icontains=search_param)
                        | Q(mobile_number__icontains=search_param)
                        | Q(
                            userlocationdetailsmodel__city_name__icontains=search_param
                        ),
                        filter_condition,
                    )
                    .order_by("rank")
                    .all()
                )
        if (request_data["filterByCategory"]) != "":
            total_categories = (
                CommitmentCategoryModel.objects.values()
                .filter(name=request_data["filterByCategory"])
                .all()
            )
        else:
            total_categories = CommitmentCategoryModel.objects.values().filter().all()
        for i in range(0, len(users_data)):
            users_data[i]["is_selected"] = False
            if challenge_id != 0:
                is_payment_done = GroupChallengesPaymentModel.objects.filter(
                    group_challenge_id=challenge_id, user_id=users_data[i]["id"]
                ).last()
                if is_payment_done is not None:
                    users_data[i]["is_payment_done"] = True
            if len(total_categories) > 1:
                commitments_data = (
                    CommitmentModel.objects.values()
                    .filter(user_id=users_data[i]["id"])
                    .all()
                )
                done_commitments_data = (
                    CommitmentModel.objects.values()
                    .filter(user_id=users_data[i]["id"], is_done=True, is_updated=True)
                    .all()
                )
                notDone_commitments_data = (
                    CommitmentModel.objects.values()
                    .filter(user_id=users_data[i]["id"], is_done=False, is_updated=True)
                    .all()
                )
                notUpdated_commitments_data = (
                    CommitmentModel.objects.values()
                    .filter(
                        user_id=users_data[i]["id"], is_done=False, is_updated=False
                    )
                    .all()
                )
                users_data[i]["commitments_details"] = {}
                users_data[i]["commitments_details"]["total_commitments"] = len(
                    commitments_data
                )
                users_data[i]["commitments_details"]["total_commitments_done"] = len(
                    done_commitments_data
                )
                users_data[i]["commitments_details"][
                    "total_commitments_not_done"
                ] = len(notDone_commitments_data)
                users_data[i]["commitments_details"][
                    "total_commitments_not_updated"
                ] = len(notUpdated_commitments_data)
                users_data[i]["commitments_details"]["category_wise"] = []
            for j in range(0, total_categories.count()):
                data = {}
                commitments_data = (
                    CommitmentModel.objects.values()
                    .filter(
                        user_id=users_data[i]["id"],
                        category=CommitmentCategoryModel(id=total_categories[j]["id"]),
                    )
                    .all()
                )
                done_commitments_data = (
                    CommitmentModel.objects.values()
                    .filter(
                        user_id=users_data[i]["id"],
                        category=CommitmentCategoryModel(id=total_categories[j]["id"]),
                        is_done=True,
                        is_updated=True,
                    )
                    .all()
                )
                notDone_commitments_data = (
                    CommitmentModel.objects.values()
                    .filter(
                        user_id=users_data[i]["id"],
                        category=CommitmentCategoryModel(id=total_categories[j]["id"]),
                        is_done=False,
                        is_updated=True,
                    )
                    .all()
                )
                notUpdated_commitments_data = (
                    CommitmentModel.objects.values()
                    .filter(
                        user_id=users_data[i]["id"],
                        category=CommitmentCategoryModel(id=total_categories[j]["id"]),
                        is_done=False,
                        is_updated=False,
                    )
                    .all()
                )
                if total_categories.count() == 1:
                    users_data[i]["commitments_details"] = {}
                    users_data[i]["commitments_details"]["total_commitments"] = len(
                        commitments_data
                    )
                    users_data[i]["commitments_details"][
                        "total_commitments_done"
                    ] = len(done_commitments_data)
                    users_data[i]["commitments_details"][
                        "total_commitments_not_done"
                    ] = len(notDone_commitments_data)
                    users_data[i]["commitments_details"][
                        "total_commitments_not_updated"
                    ] = len(notUpdated_commitments_data)
                    users_data[i]["commitments_details"]["category_wise"] = []
                data["category_name"] = total_categories[j]["name"]
                data["total_commitments"] = len(commitments_data)
                data["total_commitments_done"] = len(done_commitments_data)
                data["total_commitments_not_done"] = len(notDone_commitments_data)
                data["total_commitments_not_updated"] = len(notUpdated_commitments_data)
                users_data[i]["commitments_details"]["category_wise"].append(data)
            city = (
                UserLocationDetailsModel.objects.values()
                .filter(user=UserModel(id=users_data[i]["id"]))
                .first()
            )
            if city is not None:
                users_data[i]["city_data"] = (
                    CitiesModel.objects.values().filter(id=city["city_id"]).get()
                )
                users_data[i]["city_data"].pop("created_at")
                users_data[i]["city_data"].pop("updated_at")
            income_range_id = (
                UserProfessionalDetailsModel.objects.values()
                .filter(user=UserModel(id=users_data[i]["id"]))
                .first()
            )
            if income_range_id is not None:
                income_data = (
                    IncomeModel.objects.values()
                    .filter(id=income_range_id["income_range_id"])
                    .first()
                )
                if income_data is not None:
                    users_data[i]["income_range_data"] = income_data
                    users_data[i]["income_range_data"].pop("created_at")
                    users_data[i]["income_range_data"].pop("updated_at")
                users_data[i]["designation_data"] = (
                    DesignationModel.objects.values()
                    .filter(id=income_range_id["designation_id"])
                    .get()
                )
                users_data[i]["designation_title"] = income_range_id[
                    "designation_title"
                ]
                users_data[i]["designation_data"].pop("created_at")
                users_data[i]["designation_data"].pop("updated_at")
            healthData = (
                UserHealthDetailsModel.objects.values()
                .filter(user=UserModel(id=users_data[i]["id"]))
                .last()
            )
            if healthData is not None:
                users_data[i]["age"] = healthData["age"]
            users_data[i].pop("created_at")
            users_data[i].pop("updated_at")
            users_data[i]["privacy_details"] = {}
            userPrivacyDetails = (
                UserPrivacyModel.objects.values()
                .filter(user_id=users_data[i]["id"])
                .first()
            )
            if userPrivacyDetails is not None:
                users_data[i]["privacy_details"]["is_age_hidden"] = userPrivacyDetails[
                    "is_age_hidden"
                ]
                users_data[i]["privacy_details"][
                    "is_designation_title_hidden"
                ] = userPrivacyDetails["is_designation_title_hidden"]
                users_data[i]["privacy_details"][
                    "is_mobile_number_hidden"
                ] = userPrivacyDetails["is_mobile_number_hidden"]
            else:
                users_data[i]["privacy_details"]["is_age_hidden"] = True
                users_data[i]["privacy_details"]["is_mobile_number_hidden"] = True
                users_data[i]["privacy_details"]["is_city_hidden"] = False
                users_data[i]["privacy_details"]["is_designation_title_hidden"] = True
        if request_data["sortBy"] == "Commitment done (max to min)":
            users_data = sorted(
                users_data,
                key=lambda d: d["commitments_details"]["total_commitments_done"],
                reverse=True,
            )[start:end]
        elif request_data["sortBy"] == "Commitment done (min to max)":
            users_data = sorted(
                users_data,
                key=lambda d: d["commitments_details"]["total_commitments_done"],
                reverse=False,
            )[start:end]
        elif (
            request_data["filterByCategory"] == ""
            and request_data["filterByDesignation"] == ""
            and request_data["sortBy"] == ""
            and search_param != ""
        ):
            users_data = users_data[start:end]
        commitment_category_data = list(
            CommitmentCategoryModel.objects.values().filter()
        )
        for i in range(0, len(commitment_category_data)):
            commitment_category_data[i]["commitment_category_name_data"] = list(
                CommitmentNameModel.objects.values().filter(
                    category_id=commitment_category_data[i]["id"]
                )
            )
            for j in range(
                0, len(commitment_category_data[i]["commitment_category_name_data"])
            ):
                commitment_category_data[i]["commitment_category_name_data"][j].pop(
                    "created_at"
                )
                commitment_category_data[i]["commitment_category_name_data"][j].pop(
                    "updated_at"
                )
                commitment_category_data[i]["commitment_category_name_data"][j][
                    "isSelected"
                ] = False
            commitment_category_data[i].pop("created_at")
            commitment_category_data[i].pop("updated_at")
        if len(get_all_users) == 0:
            return Response(
                ResponseData.success_for_getting_commitments(
                    users_data, commitment_category_data, "No Data Found"
                ),
                status=status.HTTP_201_CREATED,
            )
        does_today_data_exists = LogsOfPagesOfUserModel.objects.filter(
            user_id=user_id
        ).last()
        print(f"does_today_data_exists {does_today_data_exists}")
        if does_today_data_exists is None:
            new_data = LogsOfPagesOfUserModel.objects.create(
                user_id=user_id, individual_user_performance_page=1
            )
            new_data.save()
        else:
            does_today_data_exists.individual_user_performance_page = (
                does_today_data_exists.individual_user_performance_page + 1
            )
            does_today_data_exists.save()
        return Response(
            ResponseData.success_for_getting_commitments(
                users_data,
                commitment_category_data,
                "User Details fetched successfully",
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
def getAllUnVerifiedUsers(request):
    """Function to get unverified users list"""
    try:
        users_data = (
            UserModel.objects.values()
            .filter(is_verified=False, is_admin=False)
            .order_by("-joining_date")
            .all()
        )
        for i in range(0, len(users_data)):
            city = (
                UserLocationDetailsModel.objects.values()
                .filter(user=UserModel(id=users_data[i]["id"]))
                .get()
            )
            print(city)
            if city is not None:
                users_data[i]["city_data"] = (
                    CitiesModel.objects.values().filter(id=city["city_id"]).get()
                )
                users_data[i]["city_data"].pop("created_at")
                users_data[i]["city_data"].pop("updated_at")
            income_range_id = (
                UserProfessionalDetailsModel.objects.values()
                .filter(user=UserModel(id=users_data[i]["id"]))
                .get()
            )
            if income_range_id is not None:
                #    users_data[i]['income_range_data'] = IncomeModel.objects.values().filter(id=income_range_id['income_range_id']).get()
                users_data[i]["designation_data"] = (
                    DesignationModel.objects.values()
                    .filter(id=income_range_id["designation_id"])
                    .get()
                )
                users_data[i]["designation_title"] = income_range_id[
                    "designation_title"
                ]
                users_data[i]["designation_data"].pop("created_at")
                users_data[i]["designation_data"].pop("updated_at")
            #    users_data[i]['income_range_data'].pop('created_at')
            #    users_data[i]['income_range_data'].pop('updated_at')
            user_health_details = (
                UserHealthDetailsModel.objects.values()
                .filter(user=UserModel(id=users_data[i]["id"]))
                .last()
            )
            if user_health_details is not None:
                users_data[i]["age"] = user_health_details["age"]
            users_data[i].pop("created_at")
            users_data[i].pop("updated_at")
        if users_data.count() == 0:
            return Response(
                ResponseData.success([], "No unverified user found"),
                status=status.HTTP_201_CREATED,
            )
        return Response(
            ResponseData.success(
                users_data, "Unverified Users list fetched successfully"
            ),
            status=status.HTTP_201_CREATED,
        )

    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def get_commitment_category_data():
    commitment_category_data = list(CommitmentCategoryModel.objects.values().filter())
    for i in range(0, len(commitment_category_data)):
        commitment_category_data[i]["commitment_category_name_data"] = list(
            CommitmentNameModel.objects.values().filter(
                category_id=commitment_category_data[i]["id"]
            )
        )
        for j in range(
            0, len(commitment_category_data[i]["commitment_category_name_data"])
        ):
            commitment_category_data[i]["commitment_category_name_data"][j].pop(
                "created_at"
            )
            commitment_category_data[i]["commitment_category_name_data"][j].pop(
                "updated_at"
            )
            commitment_category_data[i]["commitment_category_name_data"][j][
                "isSelected"
            ] = False
        commitment_category_data[i].pop("created_at")
        commitment_category_data[i].pop("updated_at")
    return commitment_category_data


@api_view(["POST"])
@authentication_classes(
    [
        ApiKeyAuthentication,
    ]
)
def getOverallPerformerOfTheWeek(request):
    """Function to get overall performer of the week"""
    try:
        users_data = UserModel.objects.values().filter(is_active=True).all()
        today = datetime.now()
        from_user_id = request.data["user_id"]
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        sub_start_date = datetime.strptime(str(start).split(" ")[0], "%Y-%m-%d").date()
        sub_end_date = datetime.strptime(str(end).split(" ")[0], "%Y-%m-%d").date()
        final_data = []
        for i in range(0, len(users_data)):
            max_done_commitments = {"user_id": "", "max_commitments": 0}
            users_data[i]["commitments"] = []
            max_done_commitments["user_id"] = users_data[i]["id"]
            commitment_data = (
                CommitmentModel.objects.values()
                .filter(Q(commitment_date__range=[sub_start_date, sub_end_date]))
                .filter(user_id=users_data[i]["id"], is_done=True, is_updated=True)
                .all()
            )
            max_done_commitments["max_commitments"] = len(commitment_data)
            print(f"len(commitment_data) {len(commitment_data)}")
            if len(commitment_data) != 0:
                final_data.append(max_done_commitments)
        newlist = sorted(final_data, key=lambda d: d["max_commitments"], reverse=True)
        user_ids = []
        print(newlist)
        if len(newlist) > 0:
            user_ids.append(newlist[0]["user_id"])
        for j in range(1, len(newlist)):
            if str(newlist[j]["max_commitments"]) == str(newlist[0]["max_commitments"]):
                user_ids.append(newlist[j]["user_id"])
        print("called")
        if len(user_ids) == 0:
            return Response(
                ResponseData.success([], "No Data Found"),
                status=status.HTTP_201_CREATED,
            )
        total_categories = CommitmentCategoryModel.objects.values().filter().all()
        finalData = []
        for k in range(0, len(user_ids)):
            users_data = (
                UserModel.objects.values().filter(id=user_ids[k], is_active=True).all()
            )
            for i in range(0, len(users_data)):
                commitments_data = (
                    CommitmentModel.objects.values()
                    .filter(Q(commitment_date__range=[sub_start_date, sub_end_date]))
                    .filter(user_id=users_data[i]["id"])
                    .all()
                )
                users_data[i]["commitments_details"] = {}
                users_data[i]["commitments_details"][
                    "total_commitments"
                ] = commitments_data.count()
                done_commitments_data = (
                    CommitmentModel.objects.values()
                    .filter(Q(commitment_date__range=[sub_start_date, sub_end_date]))
                    .filter(user_id=users_data[i]["id"], is_done=True, is_updated=True)
                    .all()
                )
                users_data[i]["commitments_details"][
                    "total_commitments_done"
                ] = done_commitments_data.count()
                notDone_commitments_data = (
                    CommitmentModel.objects.values()
                    .filter(Q(commitment_date__range=[sub_start_date, sub_end_date]))
                    .filter(user_id=users_data[i]["id"], is_done=False, is_updated=True)
                    .all()
                )
                users_data[i]["commitments_details"][
                    "total_commitments_not_done"
                ] = notDone_commitments_data.count()
                notUpdated_commitments_data = (
                    CommitmentModel.objects.values()
                    .filter(Q(commitment_date__range=[sub_start_date, sub_end_date]))
                    .filter(
                        user_id=users_data[i]["id"], is_done=False, is_updated=False
                    )
                    .all()
                )
                users_data[i]["commitments_details"][
                    "total_commitments_not_updated"
                ] = notUpdated_commitments_data.count()
                users_data[i]["commitments_details"]["category_wise"] = []
                for j in range(0, len(total_categories)):
                    data = {}
                    commitments_data = (
                        CommitmentModel.objects.values()
                        .filter(
                            Q(commitment_date__range=[sub_start_date, sub_end_date])
                        )
                        .filter(
                            user_id=users_data[i]["id"],
                            category=CommitmentCategoryModel(
                                id=total_categories[j]["id"]
                            ),
                        )
                        .all()
                    )
                    data["total_commitments"] = commitments_data.count()
                    done_commitments_data = (
                        CommitmentModel.objects.values()
                        .filter(
                            Q(commitment_date__range=[sub_start_date, sub_end_date])
                        )
                        .filter(
                            user_id=users_data[i]["id"],
                            category=CommitmentCategoryModel(
                                id=total_categories[j]["id"]
                            ),
                            is_done=True,
                            is_updated=True,
                        )
                        .all()
                    )
                    data["total_commitments_done"] = done_commitments_data.count()
                    notDone_commitments_data = (
                        CommitmentModel.objects.values()
                        .filter(
                            Q(commitment_date__range=[sub_start_date, sub_end_date])
                        )
                        .filter(
                            user_id=users_data[i]["id"],
                            category=CommitmentCategoryModel(
                                id=total_categories[j]["id"]
                            ),
                            is_done=False,
                            is_updated=True,
                        )
                        .all()
                    )
                    data[
                        "total_commitments_not_done"
                    ] = notDone_commitments_data.count()
                    notUpdated_commitments_data = (
                        CommitmentModel.objects.values()
                        .filter(
                            Q(commitment_date__range=[sub_start_date, sub_end_date])
                        )
                        .filter(
                            user_id=users_data[i]["id"],
                            category=CommitmentCategoryModel(
                                id=total_categories[j]["id"]
                            ),
                            is_done=False,
                            is_updated=False,
                        )
                        .all()
                    )
                    data[
                        "total_commitments_not_updated"
                    ] = notUpdated_commitments_data.count()
                    data["category_name"] = total_categories[j]["name"]
                    users_data[i]["commitments_details"]["category_wise"].append(data)
                users_data[i].pop("created_at")
                users_data[i].pop("updated_at")
                city_id = (
                    UserLocationDetailsModel.objects.values()
                    .filter(user=UserModel(id=users_data[i]["id"]))
                    .get()
                )
                if city_id is not None:
                    users_data[i]["city_data"] = (
                        CitiesModel.objects.values().filter(id=city_id["city_id"]).get()
                    )
                    users_data[i]["city_data"].pop("created_at")
                    users_data[i]["city_data"].pop("updated_at")
                    income_range_id = (
                        UserProfessionalDetailsModel.objects.values()
                        .filter(user=UserModel(id=users_data[i]["id"]))
                        .get()
                    )
                if income_range_id["income_range_id"] is not None:
                    print(f"fvfvdvdfvf {income_range_id}")
                    incomeData = (
                        IncomeModel.objects.values()
                        .filter(id=income_range_id["income_range_id"])
                        .get()
                    )
                    if incomeData is not None:
                        users_data[i]["income_range_data"] = incomeData
                        users_data[i]["income_range_data"].pop("created_at")
                        users_data[i]["income_range_data"].pop("updated_at")
                if income_range_id["designation_id"] is not None:
                    users_data[i]["designation_data"] = (
                        DesignationModel.objects.values()
                        .filter(id=income_range_id["designation_id"])
                        .get()
                    )
                    users_data[i]["designation_title"] = income_range_id[
                        "designation_title"
                    ]
                    users_data[i]["designation_data"].pop("created_at")
                    users_data[i]["designation_data"].pop("updated_at")

                users_data[i]["age"] = (
                    UserHealthDetailsModel.objects.values()
                    .filter(user=UserModel(id=users_data[i]["id"]))
                    .get()["age"]
                )
            finalData.append(users_data[i])
        does_today_data_exists = LogsOfPagesOfUserModel.objects.filter(
            user_id=from_user_id
        ).last()
        if does_today_data_exists is None:
            new_data = LogsOfPagesOfUserModel.objects.create(
                user_id=from_user_id, add_commitment_page=1
            )
            new_data.save()
        else:
            does_today_data_exists.add_commitment_page = (
                does_today_data_exists.add_commitment_page + 1
            )
            does_today_data_exists.save()
        return Response(
            ResponseData.success_with_commitment_update(
                finalData,
                get_commitment_category_data(),
                "User Details fetched successfully",
                False,
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
        for i in range(0, len(users_data)):
            max_done_commitments = {"user_id": "", "max_commitments": 0}
            users_data[i]["commitments"] = []
            max_done_commitments["user_id"] = users_data[i]["id"]
            commitment_data = (
                CommitmentModel.objects.values()
                .filter(Q(commitment_date__range=[sub_start_date, sub_end_date]))
                .filter(user_id=users_data[i]["id"], is_done=True, is_updated=True)
                .all()
            )
            max_done_commitments["max_commitments"] = len(commitment_data)
            if len(commitment_data) != 0:
                final_data.append(max_done_commitments)
        newlist = sorted(final_data, key=lambda d: d["max_commitments"], reverse=True)
        user_ids = []
        print(newlist)
        if len(newlist) > 0:
            user_ids.append(newlist[0]["user_id"])
        for j in range(1, len(newlist)):
            if str(newlist[j]["max_commitments"]) == str(newlist[0]["max_commitments"]):
                user_ids.append(newlist[j]["user_id"])
        print("called")
        if len(user_ids) == 0:
            return Response(
                ResponseData.success([], "No Data Found"),
                status=status.HTTP_201_CREATED,
            )
        total_categories = CommitmentCategoryModel.objects.values().filter().all()
        finalData = []
        for k in range(0, len(user_ids)):
            users_data = (
                UserModel.objects.values().filter(id=user_ids[k], is_active=True).all()
            )
            for i in range(0, len(users_data)):
                commitments_data = (
                    CommitmentModel.objects.values()
                    .filter(Q(commitment_date__range=[sub_start_date, sub_end_date]))
                    .filter(user_id=users_data[i]["id"])
                    .all()
                )
                users_data[i]["commitments_details"] = {}
                users_data[i]["commitments_details"][
                    "total_commitments"
                ] = commitments_data.count()
                done_commitments_data = (
                    CommitmentModel.objects.values()
                    .filter(Q(commitment_date__range=[sub_start_date, sub_end_date]))
                    .filter(user_id=users_data[i]["id"], is_done=True, is_updated=True)
                    .all()
                )
                users_data[i]["commitments_details"][
                    "total_commitments_done"
                ] = done_commitments_data.count()
                notDone_commitments_data = (
                    CommitmentModel.objects.values()
                    .filter(Q(commitment_date__range=[sub_start_date, sub_end_date]))
                    .filter(user_id=users_data[i]["id"], is_done=False, is_updated=True)
                    .all()
                )
                users_data[i]["commitments_details"][
                    "total_commitments_not_done"
                ] = notDone_commitments_data.count()
                notUpdated_commitments_data = (
                    CommitmentModel.objects.values()
                    .filter(Q(commitment_date__range=[sub_start_date, sub_end_date]))
                    .filter(
                        user_id=users_data[i]["id"], is_done=False, is_updated=False
                    )
                    .all()
                )
                users_data[i]["commitments_details"][
                    "total_commitments_not_updated"
                ] = notUpdated_commitments_data.count()
                users_data[i]["commitments_details"]["category_wise"] = []
                for j in range(0, len(total_categories)):
                    data = {}
                    commitments_data = (
                        CommitmentModel.objects.values()
                        .filter(
                            Q(commitment_date__range=[sub_start_date, sub_end_date])
                        )
                        .filter(
                            user_id=users_data[i]["id"],
                            category=CommitmentCategoryModel(
                                id=total_categories[j]["id"]
                            ),
                        )
                        .all()
                    )
                    data["total_commitments"] = commitments_data.count()
                    done_commitments_data = (
                        CommitmentModel.objects.values()
                        .filter(
                            Q(commitment_date__range=[sub_start_date, sub_end_date])
                        )
                        .filter(
                            user_id=users_data[i]["id"],
                            category=CommitmentCategoryModel(
                                id=total_categories[j]["id"]
                            ),
                            is_done=True,
                            is_updated=True,
                        )
                        .all()
                    )
                    data["total_commitments_done"] = done_commitments_data.count()
                    notDone_commitments_data = (
                        CommitmentModel.objects.values()
                        .filter(
                            Q(commitment_date__range=[sub_start_date, sub_end_date])
                        )
                        .filter(
                            user_id=users_data[i]["id"],
                            category=CommitmentCategoryModel(
                                id=total_categories[j]["id"]
                            ),
                            is_done=False,
                            is_updated=True,
                        )
                        .all()
                    )
                    data[
                        "total_commitments_not_done"
                    ] = notDone_commitments_data.count()
                    notUpdated_commitments_data = (
                        CommitmentModel.objects.values()
                        .filter(
                            Q(commitment_date__range=[sub_start_date, sub_end_date])
                        )
                        .filter(
                            user_id=users_data[i]["id"],
                            category=CommitmentCategoryModel(
                                id=total_categories[j]["id"]
                            ),
                            is_done=False,
                            is_updated=False,
                        )
                        .all()
                    )
                    data[
                        "total_commitments_not_updated"
                    ] = notUpdated_commitments_data.count()
                    data["category_name"] = total_categories[j]["name"]
                    users_data[i]["commitments_details"]["category_wise"].append(data)
                users_data[i].pop("created_at")
                users_data[i].pop("updated_at")
                city_id = (
                    UserLocationDetailsModel.objects.values()
                    .filter(user=UserModel(id=users_data[i]["id"]))
                    .get()
                )
                if city_id is not None:
                    users_data[i]["city_data"] = (
                        CitiesModel.objects.values().filter(id=city_id["city_id"]).get()
                    )
                    users_data[i]["city_data"].pop("created_at")
                    users_data[i]["city_data"].pop("updated_at")
                    income_range_id = (
                        UserProfessionalDetailsModel.objects.values()
                        .filter(user=UserModel(id=users_data[i]["id"]))
                        .get()
                    )
                if income_range_id is not None:
                    users_data[i]["income_range_data"] = (
                        IncomeModel.objects.values()
                        .filter(id=income_range_id["income_range_id"])
                        .get()
                    )
                    users_data[i]["designation_data"] = (
                        DesignationModel.objects.values()
                        .filter(id=income_range_id["designation_id"])
                        .get()
                    )
                    users_data[i]["designation_title"] = income_range_id[
                        "designation_title"
                    ]
                    users_data[i]["designation_data"].pop("created_at")
                    users_data[i]["designation_data"].pop("updated_at")
                    users_data[i]["income_range_data"].pop("created_at")
                    users_data[i]["income_range_data"].pop("updated_at")
                users_data[i]["age"] = (
                    UserHealthDetailsModel.objects.values()
                    .filter(user=UserModel(id=users_data[i]["id"]))
                    .get()["age"]
                )
            finalData.append(users_data[i])
        return Response(
            ResponseData.success(finalData, "User Details fetched successfully"),
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
        for index in range(0, len(total_categories)):
            final_data = []
            for i in range(0, len(all_users_data)):
                max_done_commitments = {"user_id": "", "max_commitments": 0}
                all_users_data[i]["commitments"] = []
                max_done_commitments["user_id"] = all_users_data[i]["id"]
                commitment_data = (
                    CommitmentModel.objects.values()
                    .filter(Q(commitment_date__range=[sub_start_date, sub_end_date]))
                    .filter(
                        user_id=all_users_data[i]["id"],
                        is_done=True,
                        is_updated=True,
                        category=CommitmentCategoryModel(
                            id=total_categories[index]["id"]
                        ),
                    )
                    .all()
                )
                value = len(commitment_data)
                max_done_commitments["max_commitments"] = value
                if value != 0:
                    final_data.append(max_done_commitments)
            newlist = sorted(
                final_data, key=lambda d: d["max_commitments"], reverse=True
            )
            user_ids = []
            if len(newlist) > 0:
                user_ids.append(newlist[0]["user_id"])
            for j in range(1, len(newlist)):
                if str(newlist[j]["max_commitments"]) == str(
                    newlist[0]["max_commitments"]
                ):
                    user_ids.append(newlist[j]["user_id"])
            finalData = []
            for k in range(0, len(user_ids)):
                users_data = (
                    UserModel.objects.values()
                    .filter(id=user_ids[k], is_active=True)
                    .all()
                )
                for i in range(0, len(users_data)):
                    commitments_data = (
                        CommitmentModel.objects.values()
                        .filter(
                            Q(commitment_date__range=[sub_start_date, sub_end_date])
                        )
                        .filter(user_id=users_data[i]["id"])
                        .all()
                    )
                    users_data[i]["commitments_details"] = {}
                    users_data[i]["commitments_details"][
                        "total_commitments"
                    ] = commitments_data.count()
                    done_commitments_data = (
                        CommitmentModel.objects.values()
                        .filter(
                            Q(commitment_date__range=[sub_start_date, sub_end_date])
                        )
                        .filter(
                            user_id=users_data[i]["id"], is_done=True, is_updated=True
                        )
                        .all()
                    )
                    users_data[i]["commitments_details"][
                        "total_commitments_done"
                    ] = done_commitments_data.count()
                    notDone_commitments_data = (
                        CommitmentModel.objects.values()
                        .filter(
                            Q(commitment_date__range=[sub_start_date, sub_end_date])
                        )
                        .filter(
                            user_id=users_data[i]["id"], is_done=False, is_updated=True
                        )
                        .all()
                    )
                    users_data[i]["commitments_details"][
                        "total_commitments_not_done"
                    ] = notDone_commitments_data.count()
                    notUpdated_commitments_data = (
                        CommitmentModel.objects.values()
                        .filter(
                            Q(commitment_date__range=[sub_start_date, sub_end_date])
                        )
                        .filter(
                            user_id=users_data[i]["id"],
                            is_done=False,
                            is_updated=False,
                        )
                        .all()
                    )
                    users_data[i]["commitments_details"][
                        "total_commitments_not_updated"
                    ] = notUpdated_commitments_data.count()
                    users_data[i]["commitments_details"]["category_wise"] = []
                    for j in range(0, len(total_categories)):
                        data = {}
                        commitments_data = (
                            CommitmentModel.objects.values()
                            .filter(
                                Q(
                                    commitment_date__range=[
                                        sub_start_date,
                                        sub_end_date,
                                    ]
                                )
                            )
                            .filter(
                                user_id=users_data[i]["id"],
                                category=CommitmentCategoryModel(
                                    id=total_categories[j]["id"]
                                ),
                            )
                            .all()
                        )
                        data["total_commitments"] = commitments_data.count()
                        done_commitments_data_category = (
                            CommitmentModel.objects.values()
                            .filter(
                                Q(
                                    commitment_date__range=[
                                        sub_start_date,
                                        sub_end_date,
                                    ]
                                )
                            )
                            .filter(
                                user_id=users_data[i]["id"],
                                category=CommitmentCategoryModel(
                                    id=total_categories[j]["id"]
                                ),
                                is_done=True,
                                is_updated=True,
                            )
                            .all()
                        )
                        data[
                            "total_commitments_done"
                        ] = done_commitments_data_category.count()
                        notDone_commitments_data = (
                            CommitmentModel.objects.values()
                            .filter(
                                Q(
                                    commitment_date__range=[
                                        sub_start_date,
                                        sub_end_date,
                                    ]
                                )
                            )
                            .filter(
                                user_id=users_data[i]["id"],
                                category=CommitmentCategoryModel(
                                    id=total_categories[j]["id"]
                                ),
                                is_done=False,
                                is_updated=True,
                            )
                            .all()
                        )
                        data[
                            "total_commitments_not_done"
                        ] = notDone_commitments_data.count()
                        notUpdated_commitments_data = (
                            CommitmentModel.objects.values()
                            .filter(
                                Q(
                                    commitment_date__range=[
                                        sub_start_date,
                                        sub_end_date,
                                    ]
                                )
                            )
                            .filter(
                                user_id=users_data[i]["id"],
                                category=CommitmentCategoryModel(
                                    id=total_categories[j]["id"]
                                ),
                                is_done=False,
                                is_updated=False,
                            )
                            .all()
                        )
                        data[
                            "total_commitments_not_updated"
                        ] = notUpdated_commitments_data.count()
                        data["category_name"] = total_categories[j]["name"]
                        users_data[i]["commitments_details"]["category_wise"].append(
                            data
                        )
                        users_data[i]["category_name"] = total_categories[index]["name"]
                users_data[i].pop("created_at")
                users_data[i].pop("updated_at")
                city_id = (
                    UserLocationDetailsModel.objects.values()
                    .filter(user=UserModel(id=users_data[i]["id"]))
                    .get()
                )
                if city_id is not None:
                    users_data[i]["city_data"] = (
                        CitiesModel.objects.values().filter(id=city_id["city_id"]).get()
                    )
                    users_data[i]["city_data"].pop("created_at")
                    users_data[i]["city_data"].pop("updated_at")
                    income_range_id = (
                        UserProfessionalDetailsModel.objects.values()
                        .filter(user=UserModel(id=users_data[i]["id"]))
                        .get()
                    )
                if income_range_id is not None:
                    #    users_data[i]['income_range_data'] = IncomeModel.objects.values().filter(id=income_range_id['income_range_id']).get()
                    users_data[i]["designation_data"] = (
                        DesignationModel.objects.values()
                        .filter(id=income_range_id["designation_id"])
                        .get()
                    )
                    users_data[i]["designation_title"] = income_range_id[
                        "designation_title"
                    ]
                    users_data[i]["designation_data"].pop("created_at")
                    users_data[i]["designation_data"].pop("updated_at")
                #    users_data[i]['income_range_data'].pop('created_at')
                #    users_data[i]['income_range_data'].pop('updated_at')
                users_data[i]["age"] = (
                    UserHealthDetailsModel.objects.values()
                    .filter(user=UserModel(id=users_data[i]["id"]))
                    .get()["age"]
                )
                finalData.append(users_data[i])
            for i in range(0, len(finalData)):
                final_next_data.append(finalData[i])
        if len(final_next_data) == 0:
            return Response(
                ResponseData.success([], "No winner found"),
                status=status.HTTP_201_CREATED,
            )
        return Response(
            ResponseData.success(final_next_data, "User Details fetched successfully"),
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
def updateProfile(request):
    """Function to update user profile"""
    try:
        data = request.data
        print(data)
        user_id = request.data["id"]
        fullName = request.data["fullName"]
        mobile_number = request.data["mobileNumber"]
        email = request.data["email"]
        profilePic = (
            request.FILES["profilePic"] if "profilePic" in request.FILES else ""
        )
        height = request.data["height"]
        weight = request.data["weight"]
        cityName = request.data["cityName"]
        stateName = request.data["stateName"]
        countryName = request.data["countryName"]
        occupationData = request.data["designationData"]
        designationTitle = request.data["designationTitle"]
        userdata = UserModel.objects.filter(id=user_id).first()
        if not userdata:
            return Response(
                ResponseData.error("User id is invalid."),
                status=status.HTTP_200_OK,
            )
        userdata.full_name = fullName
        userdata.mobile_number = mobile_number
        userdata.email = email
        if "profilePic" in request.FILES:
            userdata.profile_pic = f"static/{request.FILES['profilePic']}"
        userdata.save()
        if "profilePic" in request.FILES:
            fs = FileSystemStorage(location="static/")
            fs.save(profilePic.name, profilePic)
        userhealthdata = UserHealthDetailsModel.objects.filter(user_id=user_id).first()
        userhealthdata.weight = weight
        userhealthdata.height = height
        userhealthdata.save()
        city_id = CitiesModel.objects.values().filter(name=cityName).get()["id"]
        state_id = (
            StatesModel.objects.values().filter(state_name=stateName).get()["state_id"]
        )
        country_id = (
            CountriesModel.objects.values()
            .filter(country_name=countryName)
            .get()["country_id"]
        )
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
        designation_id = (
            DesignationModel.objects.values().filter(title=occupationData).get()["id"]
        )
        userdesignationdata.designation_id = designation_id
        userdesignationdata.save()
        updated_date = list(UserModel.objects.values().filter(id=user_id))
        return Response(
            ResponseData.success(
                updated_date[0]["id"], "User profile updated successfully"
            ),
            status=status.HTTP_201_CREATED,
        )
    except KeyError as exception:
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
def updateUserPrivacyDetails(request):
    """Function to update user privacy details"""
    try:
        data = request.data
        print(data)
        serializer = UpdateUserPrivacySerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user"]
            if serializer.data["is_age_hidden"] is not None:
                privacy_details = UserPrivacyModel.objects.filter(user_id=user_id).get()
                privacy_details.is_age_hidden = serializer.data["is_age_hidden"]
                privacy_details.save()
            elif serializer.data["is_city_hidden"] is not None:
                privacy_details = UserPrivacyModel.objects.filter(user_id=user_id).get()
                privacy_details.is_city_hidden = serializer.data["is_city_hidden"]
                privacy_details.save()
            elif serializer.data["is_mobile_number_hidden"] is not None:
                privacy_details = UserPrivacyModel.objects.filter(user_id=user_id).get()
                privacy_details.is_mobile_number_hidden = serializer.data[
                    "is_mobile_number_hidden"
                ]
                privacy_details.save()
            elif serializer.data["is_designation_title_hidden"] is not None:
                privacy_details = UserPrivacyModel.objects.filter(user_id=user_id).get()
                privacy_details.is_designation_title_hidden = serializer.data[
                    "is_designation_title_hidden"
                ]
                privacy_details.save()
            return Response(
                ResponseData.success_without_data("Details updated successfully"),
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


@api_view(["POST"])
@authentication_classes(
    [
        ApiKeyAuthentication,
    ]
)
def updateIndividualUserWisePrivacyDetails(request):
    """Function to update user privacy details for specific user"""
    try:
        data = request.data
        print(data)
        serializer = UpdateUserPrivacySerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user"]
            other_user_id = serializer.data["other_user"]
            if serializer.data["is_age_hidden"] is not None:
                privacy_details = UserWisePrivacyModel.objects.filter(
                    my_details_id=user_id, other_user_details_id=other_user_id
                ).get()
                privacy_details.is_my_age_hidden = serializer.data["is_age_hidden"]
                privacy_details.save()
            elif serializer.data["is_city_hidden"] is not None:
                privacy_details = UserWisePrivacyModel.objects.filter(
                    my_details_id=user_id, other_user_details_id=other_user_id
                ).get()
                privacy_details.is_my_city_hidden = serializer.data["is_city_hidden"]
                privacy_details.save()
            elif serializer.data["is_mobile_number_hidden"] is not None:
                privacy_details = UserWisePrivacyModel.objects.filter(
                    my_details_id=user_id, other_user_details_id=other_user_id
                ).get()
                privacy_details.is_my_mobile_number_hidden = serializer.data[
                    "is_mobile_number_hidden"
                ]
                privacy_details.save()
            elif serializer.data["is_designation_title_hidden"] is not None:
                privacy_details = UserWisePrivacyModel.objects.filter(
                    my_details_id=user_id, other_user_details_id=other_user_id
                ).get()
                privacy_details.is_my_designation_title_hidden = serializer.data[
                    "is_designation_title_hidden"
                ]
                privacy_details.save()
            return Response(
                ResponseData.success_without_data("Details updated successfully"),
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


@api_view(["POST"])
@authentication_classes([ApiKeyAuthentication])
def getUserProfileDetails(request):
    """Function to get user profile details based on user id"""
    try:
        data = request.data
        print(data)
        serializer = GetUserProfileSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["id"]
            user = UserModel.objects.filter(id=user_id, is_active=True).first()
            if not user:
                return Response(
                    ResponseData.error("User id is invalid"),
                    status=status.HTTP_201_CREATED,
                )
            user_details = (
                UserModel.objects.values().filter(id=user_id, is_active=True).all()
            )
            for i in range(0, len(user_details)):
                todays_date = str(datetime.now()).split(" ")[0]
                first_date_of_month = todays_date.replace(
                    todays_date.split("-")[2], "01"
                )
                print(f"todays_date {first_date_of_month}")
                user_details[i]["total_commitments"] = CommitmentModel.objects.filter(
                    user_id=user_details[i]["id"]
                ).count()
                user_details[i]["done_commitments"] = CommitmentModel.objects.filter(
                    user_id=user_details[i]["id"], is_done=True, is_updated=True
                ).count()
                if (user_details[i]["total_commitments"]) != 0:
                    user_details[i]["star_rating"] = (
                        user_details[i]["done_commitments"]
                        / user_details[i]["total_commitments"]
                    ) * 5
                else:
                    user_details[i]["star_rating"] = 0.0
                users_data = UserModel.objects.values().filter(is_active=True).all()
                for j in range(0, len(users_data)):
                    workoutData = (
                        WarriorsWorkoutVideosModel.objects.values()
                        .filter(user_id=users_data[i]["id"])
                        .all()
                    )
                    videos_submitted = 0
                    for k in range(0, len(workoutData)):
                        if str(workoutData[k]["workout_file"]).__contains__("mp4"):
                            videos_submitted += 1
                    users_data[j]["total_commitments_done"] = (
                        CommitmentModel.objects.filter(
                            user_id=users_data[j]["id"], is_done=True, is_updated=True
                        ).count()
                        + videos_submitted
                    )
                users_sorted_data = sorted(
                    users_data, key=lambda d: d["total_commitments_done"], reverse=True
                )
                for j in range(0, len(users_sorted_data)):
                    if users_sorted_data[j]["id"] == user_id:
                        user_details[i]["user_ranking"] = users_sorted_data[j]["rank"]
                        break
                user_details[i]["cashback"] = 0.0
                prize_money_exists = ChallengesResultModel.objects.filter(
                    user_id=user_id
                ).aggregate(total_amount=Sum("prize_money"))["total_amount"]
                if prize_money_exists is not None:
                    user_details[i]["cashback"] = float(prize_money_exists)
                user_details[i]["has_user_given_before_relationship_test"] = False
                does_data_exists = (
                    UserAnswerBeforeRelationshipModel.objects.values()
                    .filter(user_id=user_details[i]["id"])
                    .all()
                )
                if len(does_data_exists) > 0:
                    user_details[i]["has_user_given_before_relationship_test"] = True
                user_details[i].pop("created_at")
                user_details[i].pop("updated_at")
                user_details[i].pop("is_active")
                user_health_details = (
                    UserHealthDetailsModel.objects.values()
                    .filter(user=UserModel(id=user_details[i]["id"]))
                    .get()
                )
                if user_health_details is not None:
                    user_details[i]["age"] = user_health_details["age"]
                    user_details[i]["weight"] = user_health_details["weight"]
                    user_details[i]["height"] = user_health_details["height"]
                    user_details[i]["gender"] = user_health_details["gender"]
                user_subscription_details = UserPaymentDetailsModel.objects.filter(
                    user=UserModel(id=user_details[i]["id"]), is_active=True
                ).first()
                user_free_trial_details = UserFreeTrialPeriodModel.objects.filter(
                    user=UserModel(id=user_details[i]["id"])
                ).last()
                user_details[i][
                    "is_free_trial_active"
                ] = user_free_trial_details.is_active
                user_details[i][
                    "free_trial_end_date"
                ] = user_free_trial_details.end_date
                if user_subscription_details is not None:
                    subscription_data = SubscriptionModel.objects.filter(
                        id=user_subscription_details.subscription_id
                    ).last()
                    user_details[i][
                        "subscription_level_name"
                    ] = subscription_data.level_name.level
                city_id = (
                    UserLocationDetailsModel.objects.values()
                    .filter(user=UserModel(id=user_details[i]["id"]))
                    .get()
                )
                if city_id is not None:
                    user_details[i]["city_name"] = (
                        CitiesModel.objects.values()
                        .filter(id=city_id["city_id"])
                        .get()["name"]
                    )
                state_id = (
                    UserLocationDetailsModel.objects.values()
                    .filter(user=UserModel(id=user_details[i]["id"]))
                    .get()
                )
                if state_id is not None:
                    user_details[i]["state_name"] = (
                        StatesModel.objects.values()
                        .filter(state_id=state_id["state_id"])
                        .get()["state_name"]
                    )
                country_id = (
                    UserLocationDetailsModel.objects.values()
                    .filter(user=UserModel(id=user_details[i]["id"]))
                    .get()
                )
                if country_id is not None:
                    user_details[i]["country_name"] = (
                        CountriesModel.objects.values()
                        .filter(country_id=country_id["country_id"])
                        .get()["country_name"]
                    )
                income_range_id = (
                    UserProfessionalDetailsModel.objects.values()
                    .filter(user=UserModel(id=user_details[i]["id"]))
                    .get()
                )
                if income_range_id["income_range_id"] is not None:
                    user_details[i]["income_range_data"] = (
                        IncomeModel.objects.values()
                        .filter(id=income_range_id["income_range_id"])
                        .get()["income_range"]
                    )
                if income_range_id["designation_id"] is not None:
                    user_details[i]["designation_data"] = (
                        DesignationModel.objects.values()
                        .filter(id=income_range_id["designation_id"])
                        .get()["title"]
                    )
                    user_details[i]["designation_title"] = income_range_id[
                        "designation_title"
                    ]
                check_data = RedeemPointsModel.objects.values().filter().all()
                for j in range(0, check_data.count()):
                    if (
                        check_data[j]["to_user_id"] == user_id
                        and check_data[j]["is_active"]
                    ):
                        user_details[i]["redeem_point_data"] = check_data[j]
                        user_details[i]["redeem_point_data"].pop("updated_at")
                        user_details[i]["redeem_point_data"].pop("created_at")
                        user_details[i]["redeem_point_data"].pop("from_user_id")
            print(user_details)
            return Response(
                ResponseData.success(
                    user_details, " User details fetched successfully"
                ),
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


@api_view(["POST"])
@authentication_classes(
    [
        ApiKeyAuthentication,
    ]
)
def getUserPrivacyDetails(request):
    """Function to get user privacy details"""
    try:
        data = request.data
        print(data)
        serializer = GetUserProfileSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["id"]
            user = UserModel.objects.filter(id=user_id, is_active=True).first()
            if not user:
                return Response(
                    ResponseData.error("User id is invalid"),
                    status=status.HTTP_201_CREATED,
                )
            user_privacy_details = (
                UserPrivacyModel.objects.values().filter(user_id=user_id).all()
            )
            for i in range(0, len(user_privacy_details)):
                user_privacy_details[0].pop("created_at")
                user_privacy_details[0].pop("updated_at")
            return Response(
                ResponseData.success(
                    user_privacy_details, " Privacy details fetched successfully"
                ),
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


@api_view(["POST"])
@authentication_classes(
    [
        ApiKeyAuthentication,
    ]
)
def getIndividualUserWisePrivacyDetails(request):
    """Function to get user privacy details for individual user wise"""
    try:
        data = request.data
        print(data)
        serializer = GetUserProfileSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["id"]
            other_user_id = serializer.data["other_user_id"]
            user = UserModel.objects.filter(id=user_id, is_active=True).first()
            if not user:
                return Response(
                    ResponseData.error("User id is invalid"),
                    status=status.HTTP_201_CREATED,
                )
            user_privacy_details = (
                UserWisePrivacyModel.objects.values()
                .filter(my_details_id=user_id, other_user_details_id=other_user_id)
                .all()
            )
            for i in range(0, len(user_privacy_details)):
                user_privacy_details[0].pop("created_at")
                user_privacy_details[0].pop("updated_at")
            return Response(
                ResponseData.success(
                    user_privacy_details, " Privacy details fetched successfully"
                ),
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


@api_view(["POST"])
@authentication_classes(
    [
        ApiKeyAuthentication,
    ]
)
def makeUserAdmin(request):
    """Function to make a user admin"""
    try:
        data = request.data
        serializer = GetUserProfileSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["id"]
            user = UserModel.objects.filter(id=user_id, is_active=True).first()
            if not user:
                return Response(
                    ResponseData.error("User id is invalid"),
                    status=status.HTTP_201_CREATED,
                )
            user.is_admin = True
            user.save()
            return Response(
                ResponseData.success([], "User has become admin now"),
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
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@authentication_classes(
    [
        ApiKeyAuthentication,
    ]
)
def delete_user_details(request):
    """Function to delete user details"""
    try:
        data = request.data
        user_id = data["user_id"]
        is_id_valid = UserModel.objects.filter(id=user_id, is_active=True).first()
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
        UserModel.objects.filter(id=user_id, is_active=True).delete()
        return Response(
            ResponseData.success_without_data("User details deleted successfully"),
            status=status.HTTP_201_CREATED,
        )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


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
@authentication_classes(
    [
        ApiKeyAuthentication,
    ]
)
def addNewReviewOfUser(request):
    """Function to add new review given by a user"""
    try:
        data = request.data
        print(data)
        serializer = AddUserReviewSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            data_of_all_reviews = serializer.data["data_of_all_reviews"]
            user_details = UserModel.objects.filter(id=user_id).first()
            if user_details is None:
                return Response(
                    ResponseData.error("User id is invalid"),
                    status=status.HTTP_200_OK,
                )
            final_data = []
            for i in range(0, len(data_of_all_reviews)):
                review_details = ReviewModel.objects.filter(
                    id=data_of_all_reviews[i]["review_id"]
                ).first()
                if review_details is None:
                    return Response(
                        ResponseData.error("Review id is invalid"),
                        status=status.HTTP_200_OK,
                    )
                does_data_exists = UserReviewModel.objects.filter(
                    user_id=user_id,
                    review_date=str(data_of_all_reviews[i]["review_date"]).split("T")[
                        0
                    ],
                ).first()
                if does_data_exists is not None:
                    return Response(
                        ResponseData.error("This data already exists"),
                        status=status.HTTP_200_OK,
                    )
                final_data.append(
                    UserReviewModel(
                        user_id=user_id,
                        review_id=data_of_all_reviews[i]["review_id"],
                        star_rating=data_of_all_reviews[i]["star_rating"],
                        description=data_of_all_reviews[i]["description"],
                        review_date=str(data_of_all_reviews[i]["review_date"]).split(
                            "T"
                        )[0],
                    )
                )
            print(f"final_data {final_data}")
            UserReviewModel.objects.bulk_create(final_data)
            return Response(
                ResponseData.success_without_data("Review added successfully"),
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
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@authentication_classes(
    [
        ApiKeyAuthentication,
    ]
)
def addAnswersGivenByUserBeforeRelationship(request):
    """Function to add answers of questions before relationship given by a user"""
    try:
        data = request.data
        print(data)
        serializer = AddAnswersOfQuestionsBeforeRelationshipSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            data_of_all_questions = serializer.data["data_of_all_questions"]
            user_details = UserModel.objects.filter(id=user_id).first()
            if user_details is None:
                return Response(
                    ResponseData.error("User id is invalid"),
                    status=status.HTTP_200_OK,
                )
            # answer_details = UserAnswerBeforeRelationshipModel.objects.filter(
            #     user_id=user_id
            # ).first()
            # if answer_details is not None:
            #     UserAnswerBeforeRelationshipModel.objects.filter(
            #         user_id=user_id
            #     ).delete()
            final_data = []
            for i in range(0, len(data_of_all_questions)):
                question_details = QuestionsToAskBeforeModel.objects.filter(
                    id=data_of_all_questions[i]["question_id"]
                ).first()
                if question_details is None:
                    return Response(
                        ResponseData.error("Question id is invalid"),
                        status=status.HTTP_200_OK,
                    )
                answer_details = UserAnswerBeforeRelationshipModel.objects.filter(
                    user_id=user_id,
                    question_id=data_of_all_questions[i]["question_id"],
                ).last()

                if (
                    answer_details is not None
                    and answer_details.answer_id
                    != data_of_all_questions[i]["answer_id"]
                ) or answer_details is None:
                    final_data.append(
                        UserAnswerBeforeRelationshipModel(
                            user_id=user_id,
                            question_id=data_of_all_questions[i]["question_id"],
                            answer_id=data_of_all_questions[i]["answer_id"],
                        )
                    )
            print(f"final_data {final_data}")
            UserAnswerBeforeRelationshipModel.objects.bulk_create(final_data)
            return Response(
                ResponseData.success_without_data("Data added successfully"),
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
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@authentication_classes(
    [
        ApiKeyAuthentication,
    ]
)
def getUserAnswersBeforeRelationship(request):
    """Function to get user answers of before relationship"""
    try:
        data = request.data
        user_id = data["user_id"]
        user = UserModel.objects.filter(id=user_id).first()
        if not user:
            return Response(
                ResponseData.error("User id is invalid"),
                status=status.HTTP_201_CREATED,
            )
        answer_details = (
            UserAnswerBeforeRelationshipModel.objects.values("question_id", "answer_id")
            .filter(user_id=user_id)
            .all()
        )
        if len(answer_details) == 0:
            return Response(
                ResponseData.error("User answers does not exists"),
                status=status.HTTP_201_CREATED,
            )
        return Response(
            ResponseData.success(answer_details, "User answers fetched successfully"),
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
            description = serializer.data["description"]
            user_review_id = serializer.data["user_review_id"]
            user_review_details = UserReviewModel.objects.filter(
                id=user_review_id
            ).first()
            if user_review_details is None:
                return Response(
                    ResponseData.error("User review id is invalid"),
                    status=status.HTTP_200_OK,
                )
            user_details = UserModel.objects.filter(id=user_id).first()
            if user_details is None:
                return Response(
                    ResponseData.error("User id is invalid"),
                    status=status.HTTP_200_OK,
                )
            review_details = ReviewModel.objects.filter(id=review_id).first()
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
                ResponseData.success_without_data("Review updated successfully"),
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


@api_view(["POST"])
@authentication_classes(
    [
        ApiKeyAuthentication,
    ]
)
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
def get_reviews_of_all_users(request):
    """Function to get reviews of all users"""
    try:
        data = request.data
        print(data)
        serializer = GetReviewsOfAllUsersSerializer(data=data)
        if serializer.is_valid():
            page_number = int(
                serializer.data["page_no"] if "page_no" in request.data else 0
            )
            page_size_param = int(
                serializer.data["page_size"] if "page_size" in request.data else 0
            )
            star_rating = (
                serializer.data["star_rating"] if "star_rating" in request.data else ""
            )
            search = serializer.data["search"] if "search" in request.data else ""
            start_date = (
                serializer.data["start_date"] if "start_date" in request.data else ""
            )
            end_date = serializer.data["end_date"] if "end_date" in request.data else ""
            page_no = page_number
            page_size = page_size_param
            if star_rating != "":
                start_rating = int(str(star_rating).split("-")[0])
                end_rating = int(str(star_rating).split("-")[1])
            start = (page_no - 1) * page_size
            end = page_no * page_size
            get_users_id = UserReviewModel.objects.values_list("user_id").distinct()[
                start:end
            ]
            final_data = []
            print(f"get_users_id {get_users_id}")
            for i in range(0, len(get_users_id)):
                if star_rating != "" and search == "" and start_date == "":
                    user_reviews_data = (
                        UserReviewModel.objects.values()
                        .filter(user_id=get_users_id[i][0])
                        .filter(Q(star_rating__range=[start_rating, end_rating]))
                        .all()
                    )
                elif star_rating != "" and search == "" and start_date != "":
                    user_reviews_data = (
                        UserReviewModel.objects.values()
                        .filter(
                            Q(review_date__range=[start_date, end_date])
                            & Q(star_rating__range=[start_rating, end_rating])
                        )
                        .filter(user_id=get_users_id[i][0])
                        .all()
                    )
                elif star_rating != "" and search != "" and start_date == "":
                    user_reviews_data = (
                        UserReviewModel.objects.values()
                        .filter(
                            (
                                Q(user__full_name__icontains=search)
                                | Q(user__mobile_number__icontains=search)
                                | Q(description__icontains=search)
                            )
                            & (Q(star_rating__range=[start_rating, end_rating]))
                        )
                        .filter(user_id=get_users_id[i][0])
                        .all()
                    )
                elif star_rating != "" and search != "" and start_date != "":
                    user_reviews_data = (
                        UserReviewModel.objects.values()
                        .filter(
                            (
                                Q(user__full_name__icontains=search)
                                | Q(user__mobile_number__icontains=search)
                                | Q(description__icontains=search)
                            )
                            & (Q(star_rating__range=[start_rating, end_rating]))
                        )
                        .filter(Q(review_date__range=[start_date, end_date]))
                        .filter(user_id=get_users_id[i][0])
                        .all()
                    )
                elif star_rating == "" and search != "" and start_date == "":
                    user_reviews_data = (
                        UserReviewModel.objects.values()
                        .filter(
                            Q(user__full_name__icontains=search)
                            | Q(user__mobile_number__icontains=search)
                            | Q(description__icontains=search)
                        )
                        .filter(user_id=get_users_id[i][0])
                        .all()
                    )
                elif star_rating == "" and search != "" and start_date != "":
                    user_reviews_data = (
                        UserReviewModel.objects.values()
                        .filter(
                            Q(user__full_name__icontains=search)
                            | Q(user__mobile_number__icontains=search)
                            | Q(description__icontains=search)
                        )
                        .filter(Q(review_date__range=[start_date, end_date]))
                        .filter(user_id=get_users_id[i][0])
                        .all()
                    )
                elif star_rating == "" and search == "" and start_date != "":
                    user_reviews_data = (
                        UserReviewModel.objects.values()
                        .filter(Q(review_date__range=[start_date, end_date]))
                        .filter(user_id=get_users_id[i][0])
                        .all()
                    )
                else:
                    user_reviews_data = (
                        UserReviewModel.objects.values()
                        .filter(user_id=get_users_id[i][0])
                        .all()
                    )
                for j in range(0, len(user_reviews_data)):
                    # user_reviews_data[j].pop("created_at")
                    # user_reviews_data[j].pop("updated_at")
                    # user_reviews_data[j].pop("user_id")
                    user_reviews_data[j]["review_title"] = (
                        ReviewModel.objects.values()
                        .filter(id=user_reviews_data[j]["review_id"])
                        .first()["title"]
                    )
                    # user_reviews_data[j].pop("review_id")
                map = {}
                if len(user_reviews_data) > 0:
                    user_data = UserModel.objects.filter(id=get_users_id[i][0]).first()
                    if user_data is not None:
                        print(f"get_users_id[i][0] {get_users_id[i][0]}")
                        map["user_name"] = user_data.full_name
                        map["review_data"] = user_reviews_data
                        final_data.append(map)
            if len(final_data) == 0:
                return Response(
                    ResponseData.success([], "No user review found"),
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                ResponseData.success(final_data, "User Reviews fetched successfully"),
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


@api_view(["POST"])
def getActiveUsersDetails(request):
    """Function to get user id, mobile number, full name of user"""
    try:
        data = request.data
        serializer = UserSubscribedOrNotSerializer(data=data)
        if serializer.is_valid():
            id = serializer.data["id"]
            user_data = UserModel.objects.exclude(pk=id).values(
                "id", "mobile_number", "full_name"
            )
            user_data = [
                {
                    "id": entry["id"],
                    "mobile_number": str(entry["mobile_number"]),
                    "full_name": entry["full_name"],
                }
                for entry in user_data
            ]
            return Response(
                ResponseData.success(user_data, "Users details fetched successfully"),
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
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
