from datetime import datetime, timedelta
from celery import shared_task

from django.apps import apps
from django.core.files.storage import FileSystemStorage
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from challenges_result.models import ChallengesResultModel

from commdem_warriors_backend.authenticators import ApiKeyAuthentication
from commitment.models import CommitmentModel, ExerciseModel
from group_challenges.models import (
    GroupChallengeModel,
    GroupChallengesPaymentModel,
    GroupChallengeTypeModel,
    GuidelinesOfGroupChallengeModel,
    ParticipantsInGroupChallengesModel,
    PublicCustomGroupChallengesTitleModel,
    RulesOfGroupChallengeModel,
)
from group_challenges.serializers import (
    AddNewUserInGroupChallengeSerializer,
    CreateNewGroupChallengeSerializer,
    GetAllParticipantsOfGroupChallengeSerializer,
    GetAllTitlesOfPublicCustomGroupChallengeSerializer,
    GetGroupChallengesSerializer,
    UploadVideoOfUserGroupChallengeSerializer,
)
from logs.models import LogsOfPagesOfUserModel
from response import Response as ResponseData
from subscription.models import SubscriptionModel
from user.models import UserModel, UserPaymentDetailsModel


def allow_unauthenticated_access(view_func):
    """
    Custom decorator to allow unauthenticated access to a specific view.
    """

    def wrapper(request, *args, **kwargs):
        # Apply ApiKeyAuthentication only if a specific header or condition is met.
        # You can customize this condition based on your requirements.
        if "unauthenticated_access" in request.headers:
            return view_func(request, *args, **kwargs)
        else:
            return authentication_classes([ApiKeyAuthentication])(view_func)(
                request, *args, **kwargs
            )

    return wrapper


@api_view(["POST"])
@allow_unauthenticated_access
@authentication_classes([ApiKeyAuthentication])
def get_group_challenges(request):
    """Function to get subscribed users group challenges based on date"""
    try:
        data = request.data
        print(f"data12 {request.data}")
        user = UserModel.objects.filter(
            id=request.data["user_id"], is_active=True
        ).first()
        if not user:
            return Response(
                ResponseData.error("User id is invalid"),
                status=status.HTTP_200_OK,
            )
        serializer = GetGroupChallengesSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            is_my_challenges = (
                serializer.data["is_my_challenges"]
                if (serializer.data["is_my_challenges"] is True)
                else None
            )
            is_finished = (
                serializer.data["is_finished"]
                if (serializer.data["is_finished"] is True)
                else None
            )
            is_ongoing = (
                serializer.data["is_ongoing"]
                if (serializer.data["is_ongoing"] is True)
                else None
            )
            is_upcoming = (
                serializer.data["is_upcoming"]
                if (serializer.data["is_upcoming"] is True)
                else None
            )
            sort_by = serializer.data["sort_by"]
            challenge_type = serializer.data["challenge_type"]
            page_number = int(
                serializer.data["page_no"] if "page_no" in request.data else 0
            )
            page_size_param = int(
                serializer.data["page_size"] if "page_size" in request.data else 0
            )
            page_no = page_number
            page_size = page_size_param
            start = (page_no - 1) * page_size
            end = page_no * page_size
            today_date = datetime.now().date()
            if is_my_challenges is not None and is_finished is None:
                group_challenge_ids = ParticipantsInGroupChallengesModel.objects.filter(
                    user_id=user_id, challenge_type__type=challenge_type
                ).values_list("group_challenge_id", flat=True)
                challenges_data = (
                    GroupChallengeModel.objects.values()
                    .filter(
                        id__in=group_challenge_ids, challenge_type__type=challenge_type
                    )
                    .all()[start:end]
                )
            elif is_my_challenges is not None and is_finished is not None:
                group_challenge_ids = ParticipantsInGroupChallengesModel.objects.filter(
                    user_id=user_id, challenge_type__type=challenge_type
                ).values_list("group_challenge_id", flat=True)
                challenges_data = (
                    GroupChallengeModel.objects.values()
                    .filter(
                        challenge_type__type=challenge_type,
                        id__in=group_challenge_ids,
                        challenge_date__lt=today_date,
                    )
                    .all()[start:end]
                )
            elif is_finished is not None:
                challenges_data = (
                    GroupChallengeModel.objects.values()
                    .filter(
                        challenge_type__type=challenge_type,
                        challenge_date__lt=today_date,
                    )
                    .all()[start:end]
                )
            elif is_ongoing is not None:
                challenges_data = (
                    GroupChallengeModel.objects.values()
                    .filter(
                        challenge_type__type=challenge_type,
                        challenge_date__lte=today_date,
                        challenge_date__gte=today_date,
                    )
                    .all()[start:end]
                )
            elif is_upcoming is not None:
                challenges_data = (
                    GroupChallengeModel.objects.values()
                    .filter(
                        challenge_type__type=challenge_type,
                        challenge_date__gt=today_date,
                    )
                    .all()[start:end]
                )
            else:
                challenges_data = (
                    GroupChallengeModel.objects.values()
                    .filter(challenge_type__type=challenge_type)
                    .all()[start:end]
                )
            if len(challenges_data) == 0:
                return Response(
                    ResponseData.success([], "No group challenge found"),
                    status=status.HTTP_201_CREATED,
                )
            for i in range(0, len(challenges_data)):
                challenges_data[i]["suggested_workout"] = (
                    GroupChallengeModel(**challenges_data[i])
                    .suggested_workout.values("mainTitle", "id")
                    .all()
                )
                todays_date = str(datetime.now()).split(" ")[0]
                first_date_of_month = todays_date.replace(
                    todays_date.split("-")[2], "01"
                )
                total_commitments_of_user = CommitmentModel.objects.filter(
                    user_id=user_id, commitment_date__gte=first_date_of_month
                ).count()
                total_done_commitments_of_user = CommitmentModel.objects.filter(
                    user_id=user_id,
                    is_done=True,
                    is_updated=True,
                    commitment_date__gte=first_date_of_month,
                ).count()
                if (total_commitments_of_user) != 0:
                    user_rating = (
                        total_done_commitments_of_user / total_commitments_of_user
                    ) * 100
                else:
                    user_rating = 0
                challenges_data[i][
                    "is_user_rating_between_this_competition_rating"
                ] = False
                challenges_data[i]["can_upload_video"] = True
                challenges_data[i]["is_past_competition"] = False
                challenges_data[i]["is_future_competition"] = False
                subscription_details = SubscriptionModel.objects.filter(
                    id=challenges_data[i]["subscription_id"], is_active=True
                ).last()
                base_amount = 0
                if subscription_details is not None:
                    base_amount = ((subscription_details.amount) / 2)
                    challenges_data[i][
                        "subscription_level"
                    ] = subscription_details.level_name.level
                else:
                    base_amount = float(challenges_data[i]["price_to_pay"])
                    #  total_amount = (base_amount*challenges_data[i]['total_participants'])*0.95
                if user_rating > 70:
                    challenges_data[i][
                        "is_user_rating_between_this_competition_rating"
                    ] = True
                challenges_data[i]["total_participants"] = (
                    ParticipantsInGroupChallengesModel.objects.filter(
                        challenge_type__type=challenge_type,
                        group_challenge_id=challenges_data[i]["id"],
                    )
                    .all()
                    .count()
                )
                user_ids_queryset = ParticipantsInGroupChallengesModel.objects.filter(
                    challenge_type__type=challenge_type,
                    group_challenge_id=challenges_data[i]["id"],
                ).values_list("user_id", flat=True)
                print(f"user_ids_queryset {user_ids_queryset}")
                challenges_data[i]["all_participants_id"] = user_ids_queryset
                challenges_data[i]["cash_prize_distribution"] = ""
                if challenges_data[i]["total_participants"] == 1:
                    total_prize = challenges_data[i]["total_participants"] * base_amount * 0.88
                else:
                    total_prize = (
                        challenges_data[i]["total_participants"] * base_amount
                    ) * 0.88
                lowest_amount = 0.5 * base_amount
                print(f"lowest_amount {lowest_amount}")
                print(f"total_prize {total_prize}")
                challenges_data[i]["cash_pool"] = (
                    challenges_data[i]["total_participants"] * base_amount
                )
                if challenges_data[i]["total_participants"] == 1:
                    challenges_data[i]["cash_prize_distribution"] = f"{total_prize}"
                elif challenges_data[i]["total_participants"] == 2:
                    challenges_data[i][
                        "cash_prize_distribution"
                    ] = f"{0.75*total_prize} {0.25*total_prize}"
                elif challenges_data[i]["total_participants"] == 3:
                    challenges_data[i][
                        "cash_prize_distribution"
                    ] = f"{0.6*total_prize} {0.25*total_prize} {0.15*total_prize}"
                elif challenges_data[i]["total_participants"] > 3:
                    total_prize = (
                        challenges_data[i]["total_participants"] * base_amount * 0.88
                    ) - ((challenges_data[i]["total_participants"] - 3) * lowest_amount)
                    challenges_data[i][
                        "cash_prize_distribution"
                    ] = f"{0.6*total_prize} {0.25*total_prize} {0.15*total_prize} {lowest_amount}"
                challenges_data[i]["total_videos_submitted"] = len(
                    ParticipantsInGroupChallengesModel.objects.filter(
                        challenge_type__type=challenge_type,
                        group_challenge_id=challenges_data[i]["id"],
                        has_submitted_video=True,
                    ).all()
                )
                userRating = 0
                challenges_data[i]["is_user_participating"] = False
                if CommitmentModel.objects.filter(user_id=user_id).count() != 0:
                    userRating = (
                        CommitmentModel.objects.filter(
                            user_id=user_id, is_done=True, is_updated=True
                        ).count()
                        / CommitmentModel.objects.filter(user_id=user_id).count()
                    ) * 100
                subscription_data = UserPaymentDetailsModel.objects.filter(
                    user=UserModel(id=user_id), is_active=True
                ).last()
                print(f"subscription_data {subscription_data}")
                total_commitments_of_user = CommitmentModel.objects.filter(
                    user_id=user_id
                ).count()
                done_commitments_of_user = CommitmentModel.objects.filter(
                    user_id=user_id, is_done=True, is_updated=True
                ).count()
                if (total_commitments_of_user) != 0:
                    userRating = (
                        done_commitments_of_user / total_commitments_of_user
                    ) * 5
                else:
                    userRating = 0.0
                if userRating < 70:
                    challenges_data[i]["can_upload_video"] = False
                    challenges_data[i][
                        "reason_to_not_upload_video"
                    ] = "Your rating is below 70%. You cannot upload video"
                if challenges_data[i]["challenge_date"] < today_date:
                    challenges_data[i]["is_past_competition"] = True
                if challenges_data[i]["challenge_date"] > today_date:
                    challenges_data[i]["is_future_competition"] = True
                # start_date_of_week = str(datetime.now() - timedelta(days=7)).split(" ")[0]
                ten_days_ago = datetime.now() - timedelta(days=10)
                exerciseCommitments = ExerciseModel.objects.filter(
                    user_id=user_id, created_at__gte=ten_days_ago
                ).values()
                challenges_data[i]["challenge_rules"] = (
                    RulesOfGroupChallengeModel.objects.values().filter().all()
                )
                for j in range(0, len(challenges_data[i]["challenge_rules"])):
                    challenges_data[i]["challenge_rules"][j].pop("created_at")
                    challenges_data[i]["challenge_rules"][j].pop("updated_at")
                challenges_data[i]["challenge_guidelines"] = (
                    GuidelinesOfGroupChallengeModel.objects.values().filter().all()
                )
                for j in range(0, len(challenges_data[i]["challenge_guidelines"])):
                    challenges_data[i]["challenge_guidelines"][j].pop("created_at")
                    challenges_data[i]["challenge_guidelines"][j].pop("updated_at")
                    challenges_data[i]["challenge_guidelines"][j].pop(
                        "group_challenge_id"
                    )
                challenges_data[i]["has_user_submitted_video"] = False
                challenges_data[i]["challenge_video"] = ""
                print(challenges_data[i]["id"])
                is_user_participant = ParticipantsInGroupChallengesModel.objects.filter(
                    challenge_type__type=challenge_type,
                    user_id=user_id,
                    group_challenge_id=challenges_data[i]["id"],
                ).first()
                if is_user_participant is not None:
                    challenges_data[i]["is_user_participating"] = True
                    challenges_data[i][
                        "has_user_submitted_video"
                    ] = is_user_participant.has_submitted_video
                    if challenges_data[i]["has_user_submitted_video"]:
                        challenges_data[i]["challenge_video"] = str(
                            is_user_participant.challenge_video.path
                        ).split("/")[
                            len(
                                str(is_user_participant.challenge_video.path).split("/")
                            )
                            - 1
                        ]
                if is_user_participant is not None:
                    challenges_data[i]["is_user_participating"] = True
                for j in range(0, len(exerciseCommitments)):
                    if (
                        exerciseCommitments[j]["did_speak_before"] is False
                        and exerciseCommitments[j]["did_speak_positive_affirmation"]
                        is False
                    ) or (
                        exerciseCommitments[j]["did_speak_before"]
                        and exerciseCommitments[j]["did_speak_positive_affirmation"]
                        is False
                    ):
                        challenges_data[i]["can_upload_video"] = False
                        challenges_data[i][
                            "reason_to_not_upload_video"
                        ] = "You kept workout update incomplete. You cannot upload video"
                        break
            challenges_data = sorted(
                challenges_data, key=lambda d: d["created_at"], reverse=True
            )
            if sort_by is not None:
                if sort_by == "Latest to Oldest":
                    challenges_data = sorted(
                        challenges_data, key=lambda d: d["created_at"], reverse=True
                    )
                elif sort_by == "Oldest to Latest":
                    challenges_data = sorted(
                        challenges_data, key=lambda d: d["created_at"]
                    )
                elif sort_by == "Max to min participants":
                    challenges_data = sorted(
                        challenges_data,
                        key=lambda d: d["total_participants"],
                        reverse=True,
                    )
                elif sort_by == "Min to max participants":
                    challenges_data = sorted(
                        challenges_data, key=lambda d: d["total_participants"]
                    )
            for i in range(0, len(challenges_data)):
                challenges_data[i].pop("created_at")
                challenges_data[i].pop("updated_at")
            does_today_data_exists = LogsOfPagesOfUserModel.objects.filter(
                user_id=user_id
            ).last()
            if does_today_data_exists is None:
                new_data = LogsOfPagesOfUserModel.objects.create(
                    user_id=user_id, group_challenges_page=1
                )
                new_data.save()
            else:
                does_today_data_exists.group_challenges_page = (
                    does_today_data_exists.group_challenges_page + 1
                )
                does_today_data_exists.save()
            return Response(
                ResponseData.success(
                    challenges_data, "Challenges fetched successfully"
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


# # Create your views here.
# @api_view(["POST"])
# @authentication_classes([ApiKeyAuthentication])
# def get_all_bidding_group_challenges(request):
#     """Function to get bidding group challenges based on date"""
#     try:
#         data = request.data
#         print(f"data {data}")
#         user = UserModel.objects.filter(id=request.data['user_id'],is_active=True).first()
#         if not user:
#                    return Response(
#                        ResponseData.error("User id is invalid"),
#                        status=status.HTTP_200_OK,
#                    )
#         serializer = GetGroupChallengesSerializer(data=data)
#         if serializer.is_valid():
#             print("true")
#             user_id = serializer.data['user_id']
#             is_my_challenges = serializer.data['is_my_challenges'] if(serializer.data['is_my_challenges'] == True) else None
#             is_finished = serializer.data['is_finished'] if(serializer.data['is_finished'] == True) else None
#             is_ongoing = serializer.data['is_ongoing'] if(serializer.data['is_ongoing'] == True) else None
#             is_upcoming = serializer.data['is_upcoming'] if(serializer.data['is_upcoming'] == True) else None
#             sort_by = serializer.data['sort_by']
#             page_number = int(serializer.data['page_no'] if 'page_no' in request.data else 0)
#             page_size_param = int(serializer.data['page_size'] if 'page_size' in request.data else 0)
#             page_no = page_number
#             page_size = page_size_param
#             start=(page_no-1)*page_size
#             end=page_no*page_size
#             today_date = datetime.now().date()
#             if is_my_challenges is not None and is_finished is None:
#                 group_challenge_ids = ParticipantsInBiddingGroupChallengesModel.objects.filter(user_id=user_id).values_list('group_challenge_id', flat=True)
#                 challenges_data = BiddingGroupChallengesModel.objects.values().filter(id__in=group_challenge_ids).all()[start:end]
#             elif is_my_challenges is not None and is_finished is not None:
#                 group_challenge_ids = ParticipantsInBiddingGroupChallengesModel.objects.filter(user_id=user_id).values_list('group_challenge_id', flat=True)
#                 challenges_data = BiddingGroupChallengesModel.objects.values().filter(id__in=group_challenge_ids,challenge_date__lt=today_date).all()[start:end]
#             elif is_finished is not None:
#                 challenges_data = BiddingGroupChallengesModel.objects.values().filter(challenge_date__lt=today_date).all()[start:end]
#             elif is_ongoing is not None:
#                 challenges_data = BiddingGroupChallengesModel.objects.values().filter(challenge_date__lte=today_date,challenge_date__gte=today_date).all()[start:end]
#             elif is_upcoming is not None:
#                 challenges_data = BiddingGroupChallengesModel.objects.values().filter(challenge_date__gt=today_date).all()[start:end]
#             else:
#                 challenges_data = BiddingGroupChallengesModel.objects.values().filter().all()[start:end]
#             if len(challenges_data) == 0:
#                     return Response(
#                        ResponseData.success(
#                            [], "No bidding group challenge found"),
#                        status=status.HTTP_201_CREATED)
#             for i in range(0,len(challenges_data)):
#                 challenges_data[i]['suggested_workout'] = BiddingGroupChallengesModel(**challenges_data[i]).suggested_workout.values('mainTitle','id').all()
#                 challenges_data[i]['is_participation_allowed'] = False
#                 challenges_data[i]['is_past_competition'] = False
#                 challenges_data[i]['is_bidding_challenge'] = True
#                 challenges_data[i]['is_future_competition'] = False
#                 challenges_data[i]['total_participants'] = ParticipantsInBiddingGroupChallengesModel.objects.filter(group_challenge_id=challenges_data[i]['id']).all().count()
#                 challenges_data[i]['cash_prize_distribution'] = ''
#                 base_amount = float(challenges_data[i]['price_to_pay'])
#                 total_amount = (base_amount*challenges_data[i]['total_participants'])*0.95
#                 print(f"total_amount {total_amount}")
#                 if(challenges_data[i]['total_participants'] == 1):
#                     challenges_data[i]['cash_prize_distribution'] = f'{total_amount}'
#                 elif(challenges_data[i]['total_participants'] == 2):
#                     challenges_data[i]['cash_prize_distribution'] = f'{total_amount}'
#                 elif(challenges_data[i]['total_participants'] == 3):
#                     challenges_data[i]['cash_prize_distribution'] = f'{0.8*total_amount} {0.2*total_amount}'
#                 elif(challenges_data[i]['total_participants'] == 4):
#                     challenges_data[i]['cash_prize_distribution'] = f'{0.7*total_amount} {0.15*total_amount} {0.15*total_amount}'
#                 elif(challenges_data[i]['total_participants'] == 5):
#                     challenges_data[i]['cash_prize_distribution'] = f'{0.6*total_amount} {0.3*total_amount} {0.2*total_amount} {0.1*total_amount}'
#                 elif(challenges_data[i]['total_participants'] != 0):
#                     challenges_data[i]['cash_prize_distribution'] = f'{0.5*total_amount} {0.2*total_amount} {0.2*total_amount} {0.05*total_amount} {0.05*total_amount}'
#                 challenges_data[i]['cash_pool'] = total_amount
#                 challenges_data[i]['total_videos_submitted'] = len(ParticipantsInBiddingGroupChallengesModel.objects.filter(group_challenge_id=challenges_data[i]['id'],has_submitted_video=True).all())
#                 challenges_data[i]['is_user_participating'] = False
#                 user_ids_queryset = ParticipantsInBiddingGroupChallengesModel.objects.filter(group_challenge_id=challenges_data[i]['id']).values_list('user_id', flat=True)
#                 print(f"user_ids_queryset {user_ids_queryset}")
#                 challenges_data[i]['all_participants_id'] = user_ids_queryset
#                 if(challenges_data[i]['challenge_date'] < today_date ):
#                     challenges_data[i]['is_past_competition'] = True
#                 if(challenges_data[i]['challenge_date'] > today_date ):
#                     challenges_data[i]['is_future_competition'] = True
#                 if(challenges_data[i]['total_participants'] <= int(challenges_data[i]['max_participants_allowed']) and challenges_data[i]['is_future_competition']):
#                     challenges_data[i]['is_participation_allowed'] = True
#                 challenges_data[i]['challenge_rules'] = RulesOfGroupChallengeModel.objects.values().filter().all()
#                 for j in range(0,len(challenges_data[i]['challenge_rules'])):
#                     challenges_data[i]['challenge_rules'][j].pop('created_at')
#                     challenges_data[i]['challenge_rules'][j].pop('updated_at')
#                 challenges_data[i]['challenge_guidelines'] = GuidelinesOfGroupChallengeModel.objects.values().filter().all()
#                 for j in range(0,len(challenges_data[i]['challenge_guidelines'])):
#                     challenges_data[i]['challenge_guidelines'][j].pop('created_at')
#                     challenges_data[i]['challenge_guidelines'][j].pop('updated_at')
#                     challenges_data[i]['challenge_guidelines'][j].pop('group_challenge_id')
#                 challenges_data[i]['has_user_submitted_video'] = False
#                 challenges_data[i]['challenge_video'] = ''
#                 print(challenges_data[i]['id'])
#                 is_user_participant = ParticipantsInBiddingGroupChallengesModel.objects.filter(user_id=user_id,group_challenge_id=challenges_data[i]['id']).first()
#                 if is_user_participant is not None:
#                     challenges_data[i]['is_user_participating'] = True
#                     challenges_data[i]['has_user_submitted_video'] = is_user_participant.has_submitted_video
#                     if challenges_data[i]['has_user_submitted_video']:
#                         challenges_data[i]['challenge_video'] = str(is_user_participant.challenge_video.path).split("/")[len(str(is_user_participant.challenge_video.path).split("/")) - 1]
#             challenges_data = sorted(challenges_data, key=lambda d: d['created_at'],reverse=True)
#             if(sort_by is not None):
#                 if(sort_by == 'Latest to Oldest'):
#                     challenges_data = sorted(challenges_data, key=lambda d: d['created_at'],reverse=True)
#                 elif(sort_by == 'Oldest to Latest'):
#                     challenges_data = sorted(challenges_data, key=lambda d: d['created_at'])
#                 elif(sort_by == 'Max to min participants'):
#                     challenges_data = sorted(challenges_data, key=lambda d: d['total_participants'],reverse=True)
#                 elif(sort_by == 'Min to max participants'):
#                     challenges_data = sorted(challenges_data, key=lambda d: d['total_participants'])
#             for i in range(0,len(challenges_data)):
#                 challenges_data[i].pop('created_at')
#                 challenges_data[i].pop('updated_at')
#             does_today_data_exists = LogsOfPagesOfUserModel.objects.filter(user_id=user_id).last()
#             if does_today_data_exists is None:
#                 new_data = LogsOfPagesOfUserModel.objects.create(
#                     user_id=user_id,
#                     group_challenges_page = 1
#                 )
#                 new_data.save()
#             else:
#                 does_today_data_exists.group_challenges_page = does_today_data_exists.group_challenges_page + 1
#                 does_today_data_exists.save()
#             return Response(
#                        ResponseData.success(
#                            challenges_data, "Challenges fetched successfully"),
#                        status=status.HTTP_201_CREATED)
#         return Response(
#                     ResponseData.error(serializer.errors),
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#     except Exception as exception:
#         return Response(
#             ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )

# @api_view(["POST"])
# @authentication_classes([ApiKeyAuthentication])
# def get_all_free_trial_challenges(request):
#     """Function to get free trial users group challenges based on date"""
#     try:
#         data = request.data
#         print(f"data {data}")
#         user = UserModel.objects.filter(id=request.data['user_id'],is_active=True).first()
#         if not user:
#                    return Response(
#                        ResponseData.error("User id is invalid"),
#                        status=status.HTTP_200_OK,
#                    )
#         serializer = GetGroupChallengesSerializer(data=data)
#         if serializer.is_valid():
#             user_id = serializer.data['user_id']
#             is_my_challenges = serializer.data['is_my_challenges'] if(serializer.data['is_my_challenges'] == True) else None
#             is_finished = serializer.data['is_finished'] if(serializer.data['is_finished'] == True) else None
#             is_ongoing = serializer.data['is_ongoing'] if(serializer.data['is_ongoing'] == True) else None
#             is_upcoming = serializer.data['is_upcoming'] if(serializer.data['is_upcoming'] == True) else None
#             sort_by = serializer.data['sort_by']
#             page_number = int(serializer.data['page_no'] if 'page_no' in request.data else 0)
#             page_size_param = int(serializer.data['page_size'] if 'page_size' in request.data else 0)
#             page_no = page_number
#             page_size = page_size_param
#             start=(page_no-1)*page_size
#             end=page_no*page_size
#             today_date = datetime.now().date()
#             if is_my_challenges is not None and is_finished is None:
#                 group_challenge_ids = ParticipantsInGroupChallengesForFreeTrialModel.objects.filter(user_id=user_id,is_active=True).values_list('group_challenge_id', flat=True)
#                 challenges_data = GroupChallengesForFreeTrialModel.objects.values().filter(id__in=group_challenge_ids).all()[start:end]
#             elif is_my_challenges is not None and is_finished is not None:
#                 group_challenge_ids = ParticipantsInGroupChallengesForFreeTrialModel.objects.filter(user_id=user_id,is_active=True).values_list('group_challenge_id', flat=True)
#                 challenges_data = GroupChallengesForFreeTrialModel.objects.values().filter(id__in=group_challenge_ids,challenge_date__lt=today_date).all()[start:end]
#             elif is_finished is not None:
#                 challenges_data = GroupChallengesForFreeTrialModel.objects.values().filter(challenge_date__lt=today_date).all()[start:end]
#             elif is_ongoing is not None:
#                 challenges_data = GroupChallengesForFreeTrialModel.objects.values().filter(challenge_date__lte=today_date,challenge_date__gte=today_date).all()[start:end]
#             elif is_upcoming is not None:
#                 challenges_data = GroupChallengesForFreeTrialModel.objects.values().filter(challenge_date__gt=today_date).all()[start:end]
#             else:
#                 challenges_data = GroupChallengesForFreeTrialModel.objects.values().filter().all()[start:end]
#             if len(challenges_data) == 0:
#                     return Response(
#                        ResponseData.success(
#                            [], "No group challenge found"),
#                        status=status.HTTP_201_CREATED)
#             for i in range(0,len(challenges_data)):
#                 challenges_data[i]['suggested_workout'] = GroupChallengesForFreeTrialModel(**challenges_data[i]).suggested_workout.values('mainTitle','id').all()
#                 todays_date = str(datetime.now()).split(" ")[0]
#                 first_date_of_month = todays_date.replace(todays_date.split("-")[2],'01')
#                 total_commitments_of_user = CommitmentModel.objects.filter(user_id=user_id,commitment_date__gte=first_date_of_month).count()
#                 total_done_commitments_of_user = CommitmentModel.objects.filter(user_id=user_id,is_done=True,is_updated=True,commitment_date__gte=first_date_of_month).count()
#                 if (total_commitments_of_user) != 0:
#                    user_rating = (total_done_commitments_of_user/total_commitments_of_user)*100
#                 else:
#                    user_rating = 0
#                 challenges_data[i]['is_user_rating_between_this_competition_rating'] = False
#                 challenges_data[i]['is_participation_allowed'] = False
#                 challenges_data[i]['is_past_competition'] = False
#                 challenges_data[i]['is_future_competition'] = False
#                 if(user_rating > 70):
#                     challenges_data[i]['is_user_rating_between_this_competition_rating'] = True
#                 user_ids_queryset = ParticipantsInGroupChallengesForFreeTrialModel.objects.filter(group_challenge_id=challenges_data[i]['id'],is_active=True).values_list('user_id', flat=True)
#                 print(f"user_ids_queryset {user_ids_queryset}")
#                 challenges_data[i]['all_participants_id'] = user_ids_queryset
#                 challenges_data[i]['total_participants'] = ParticipantsInGroupChallengesForFreeTrialModel.objects.filter(group_challenge_id=challenges_data[i]['id'],is_active=True).all().count()
#                 challenges_data[i]['cash_prize_distribution'] = ''
#                 if((challenges_data[i]['is_limited_time_challenge'] == False)):
#                     if(challenges_data[i]['total_participants'] == 1):
#                         challenges_data[i]['cash_prize_distribution'] = '300'
#                     elif(challenges_data[i]['total_participants'] == 2):
#                         challenges_data[i]['cash_prize_distribution'] = '450'
#                     elif(challenges_data[i]['total_participants'] == 3):
#                         challenges_data[i]['cash_prize_distribution'] = '600'
#                     elif(challenges_data[i]['total_participants'] == 4):
#                         challenges_data[i]['cash_prize_distribution'] = '750'
#                     elif(challenges_data[i]['total_participants'] == 5):
#                         challenges_data[i]['cash_prize_distribution'] = '900'
#                     elif(challenges_data[i]['total_participants'] == 6):
#                         challenges_data[i]['cash_prize_distribution'] = '900 300'
#                     elif(challenges_data[i]['total_participants'] == 7):
#                         challenges_data[i]['cash_prize_distribution'] = '1050 300'
#                     elif(challenges_data[i]['total_participants'] == 8):
#                         challenges_data[i]['cash_prize_distribution'] = '1200 300'
#                     elif(challenges_data[i]['total_participants'] == 9):
#                         challenges_data[i]['cash_prize_distribution'] = '1350 300'
#                     elif(challenges_data[i]['total_participants'] != 0):
#                         print(f"challenges_data[i][''] {challenges_data[i]['is_for_free_trial']}")
#                 challenges_data[i]['cash_pool'] = 2000
#                 challenges_data[i]['total_videos_submitted'] = len(ParticipantsInGroupChallengesForFreeTrialModel.objects.filter(group_challenge_id=challenges_data[i]['id'],has_submitted_video=True).all())
#                 userRating = 0
#                 challenges_data[i]['is_user_participating'] = False
#                 if CommitmentModel.objects.filter(user_id=user_id).count() != 0:
#                     userRating = (CommitmentModel.objects.filter(user_id=user_id,is_done=True,is_updated=True).count()/CommitmentModel.objects.filter(user_id=user_id).count())*100
#                 subscription_data = UserPaymentDetailsModel.objects.filter(
#                 user=UserModel(id=user_id),is_active = True).last()
#                 total_commitments_of_user = CommitmentModel.objects.filter(user_id=user_id).count()
#                 done_commitments_of_user = CommitmentModel.objects.filter(user_id=user_id,is_done=True,is_updated=True).count()
#                 if (total_commitments_of_user) != 0:
#                    userRating = (done_commitments_of_user/total_commitments_of_user)*5
#                 else:
#                    userRating = 0.0
#                 if challenges_data[i]['challenge_date'] > today_date and subscription_data is None and userRating > 70:
#                     challenges_data[i]['is_participation_allowed'] = True
#                 if(userRating < 70):
#                     challenges_data[i]['can_upload_video'] = False
#                     challenges_data[i]['reason_to_not_upload_video'] = 'Your rating is below 70%. You cannot upload video'
#                 if(challenges_data[i]['challenge_date'] < today_date ):
#                     challenges_data[i]['is_past_competition'] = True
#                 if(challenges_data[i]['challenge_date'] > today_date ):
#                     challenges_data[i]['is_future_competition'] = True
#                 ten_days_ago = datetime.now() - timedelta(days=10)
#                 exerciseCommitments = ExerciseModel.objects.filter(user_id=user_id, created_at__gte=ten_days_ago).values()
#                 challenges_data[i]['challenge_rules'] = RulesOfGroupChallengeModel.objects.values().filter().all()
#                 for j in range(0,len(challenges_data[i]['challenge_rules'])):
#                     challenges_data[i]['challenge_rules'][j].pop('created_at')
#                     challenges_data[i]['challenge_rules'][j].pop('updated_at')
#                 challenges_data[i]['challenge_guidelines'] = GuidelinesOfGroupChallengeModel.objects.values().filter().all()
#                 for j in range(0,len(challenges_data[i]['challenge_guidelines'])):
#                     challenges_data[i]['challenge_guidelines'][j].pop('created_at')
#                     challenges_data[i]['challenge_guidelines'][j].pop('updated_at')
#                     challenges_data[i]['challenge_guidelines'][j].pop('group_challenge_id')
#                 challenges_data[i]['has_user_submitted_video'] = False
#                 challenges_data[i]['challenge_video'] = ''
#                 print(challenges_data[i]['id'])
#                 is_user_participant = ParticipantsInGroupChallengesForFreeTrialModel.objects.filter(user_id=user_id,group_challenge_id=challenges_data[i]['id']).first()
#                 if is_user_participant is not None:
#                     challenges_data[i]['is_user_participating'] = True
#                     challenges_data[i]['has_user_submitted_video'] = is_user_participant.has_submitted_video
#                     if challenges_data[i]['has_user_submitted_video']:
#                         challenges_data[i]['challenge_video'] = str(is_user_participant.challenge_video.path).split("/")[len(str(is_user_participant.challenge_video.path).split("/")) - 1]
#                 if is_user_participant is not None:
#                     challenges_data[i]['is_user_participating'] = True
#                 for j in range(0,len(exerciseCommitments)):
#                     if((exerciseCommitments[j]['did_speak_before'] == False and exerciseCommitments[j]['did_speak_positive_affirmation'] == False)
#                        or (exerciseCommitments[j]['did_speak_before'] and exerciseCommitments[j]['did_speak_positive_affirmation'] == False)):
#                         challenges_data[i]['can_upload_video'] = False
#                         challenges_data[i]['reason_to_not_upload_video'] = 'You kept workout update incomplete. You cannot upload video'
#                         break
#             challenges_data = sorted(challenges_data, key=lambda d: d['created_at'],reverse=True)
#             if(sort_by is not None):
#                 if(sort_by == 'Latest to Oldest'):
#                     challenges_data = sorted(challenges_data, key=lambda d: d['created_at'],reverse=True)
#                 elif(sort_by == 'Oldest to Latest'):
#                     challenges_data = sorted(challenges_data, key=lambda d: d['created_at'])
#                 elif(sort_by == 'Max to min participants'):
#                     challenges_data = sorted(challenges_data, key=lambda d: d['total_participants'],reverse=True)
#                 elif(sort_by == 'Min to max participants'):
#                     challenges_data = sorted(challenges_data, key=lambda d: d['total_participants'])
#             for i in range(0,len(challenges_data)):
#                 challenges_data[i].pop('created_at')
#                 challenges_data[i].pop('updated_at')
#             does_today_data_exists = LogsOfPagesOfUserModel.objects.filter(user_id=user_id).last()
#             if does_today_data_exists is None:
#                 new_data = LogsOfPagesOfUserModel.objects.create(
#                     user_id=user_id,
#                     group_challenges_page = 1
#                 )
#                 new_data.save()
#             else:
#                 does_today_data_exists.group_challenges_page = does_today_data_exists.group_challenges_page + 1
#                 does_today_data_exists.save()
#             return Response(
#                        ResponseData.success(
#                            challenges_data, "Challenges fetched successfully"),
#                        status=status.HTTP_201_CREATED)
#         return Response(
#                     ResponseData.error(serializer.errors),
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#     except Exception as exception:
#         return Response(
#             ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )


@api_view(["POST"])
@authentication_classes(
    [
        ApiKeyAuthentication,
    ]
)
def get_all_public_custom_group_challenges_title(request):
    """Function to get all titles of public custom created group challenges"""
    try:
        data = request.data
        serializer = GetAllTitlesOfPublicCustomGroupChallengeSerializer(data=data)
        if serializer.is_valid():
            serializer.data["user_id"]
            challenge_title_details = (
                PublicCustomGroupChallengesTitleModel.objects.filter(
                    is_active=True
                ).values("id", "challenge_title")
            )
            return Response(
                ResponseData.success(
                    challenge_title_details, "Challenges title fetched successfully"
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


# @api_view(["POST"])
# @authentication_classes([ApiKeyAuthentication])
# def get_all_public_custom_group_challenges(request):
#     """Function to get subscribed users group challenges based on date"""
#     try:
#         data = request.data
#         print(f"data {data}")
#         user = UserModel.objects.filter(
#             id=request.data["user_id"], is_active=True
#         ).first()
#         if not user:
#             return Response(
#                 ResponseData.error("User id is invalid"),
#                 status=status.HTTP_200_OK,
#             )
#         serializer = GetGroupChallengesSerializer(data=data)
#         if serializer.is_valid():
#             user_id = serializer.data["user_id"]
#             is_my_challenges = (
#                 serializer.data["is_my_challenges"]
#                 if (serializer.data["is_my_challenges"] == True)
#                 else None
#             )
#             is_finished = (
#                 serializer.data["is_finished"]
#                 if (serializer.data["is_finished"] == True)
#                 else None
#             )
#             is_ongoing = (
#                 serializer.data["is_ongoing"]
#                 if (serializer.data["is_ongoing"] == True)
#                 else None
#             )
#             is_upcoming = (
#                 serializer.data["is_upcoming"]
#                 if (serializer.data["is_upcoming"] == True)
#                 else None
#             )
#             sort_by = serializer.data["sort_by"]
#             page_number = int(
#                 serializer.data["page_no"] if "page_no" in request.data else 0
#             )
#             page_size_param = int(
#                 serializer.data["page_size"] if "page_size" in request.data else 0
#             )
#             page_no = page_number
#             page_size = page_size_param
#             start = (page_no - 1) * page_size
#             end = page_no * page_size
#             today_date = datetime.now().date()
#             if is_my_challenges is not None and is_finished is None:
#                 group_challenge_ids = (
#                     ParticipantsInPublicCustomGroupChallengesModel.objects.filter(
#                         user_id=user_id
#                     ).values_list("group_challenge_id", flat=True)
#                 )
#                 challenges_data = (
#                     PublicCustomGroupChallengesModel.objects.values()
#                     .filter(id__in=group_challenge_ids)
#                     .all()[start:end]
#                 )
#             elif is_my_challenges is not None and is_finished is not None:
#                 group_challenge_ids = (
#                     ParticipantsInPublicCustomGroupChallengesModel.objects.filter(
#                         user_id=user_id
#                     ).values_list("group_challenge_id", flat=True)
#                 )
#                 challenges_data = (
#                     PublicCustomGroupChallengesModel.objects.values()
#                     .filter(id__in=group_challenge_ids, challenge_date__lt=today_date)
#                     .all()[start:end]
#                 )
#             if is_finished is not None:
#                 challenges_data = (
#                     PublicCustomGroupChallengesModel.objects.values()
#                     .filter(challenge_date__lt=today_date)
#                     .all()[start:end]
#                 )
#             elif is_ongoing is not None:
#                 challenges_data = (
#                     PublicCustomGroupChallengesModel.objects.values()
#                     .filter(
#                         challenge_date__lte=today_date, challenge_date__gte=today_date
#                     )
#                     .all()[start:end]
#                 )
#             elif is_upcoming is not None:
#                 challenges_data = (
#                     PublicCustomGroupChallengesModel.objects.values()
#                     .filter(challenge_date__gt=today_date)
#                     .all()[start:end]
#                 )
#             else:
#                 challenges_data = (
#                     PublicCustomGroupChallengesModel.objects.values()
#                     .filter()
#                     .all()[start:end]
#                 )
#             if len(challenges_data) == 0:
#                 return Response(
#                     ResponseData.success([], "No group challenge found"),
#                     status=status.HTTP_201_CREATED,
#                 )
#             for i in range(0, len(challenges_data)):
#                 challenge_title_details = (
#                     PublicCustomGroupChallengesTitleModel.objects.filter(
#                         id=challenges_data[i]["challenge_details_id"]
#                     ).last()
#                 )
#                 challenges_data[i]["suggested_workout"] = (
#                     PublicCustomGroupChallengesModel(**challenges_data[i])
#                     .challenge_details.suggested_workout.values("mainTitle", "id")
#                     .all()
#                 )
#                 challenges_data[i][
#                     "is_user_rating_between_this_competition_rating"
#                 ] = False
#                 challenges_data[i]["is_participation_allowed"] = False
#                 challenges_data[i]["is_past_competition"] = False
#                 challenges_data[i]["is_future_competition"] = False
#                 challenges_data[i]["is_for_free_trial"] = True
#                 challenges_data[i]["is_bidding_challenge"] = True
#                 challenges_data[i][
#                     "challenge_name"
#                 ] = challenge_title_details.challenge_title
#                 challenges_data[i]["challenge_image"] = (
#                     os.path.basename(challenge_title_details.challenge_image.path)
#                     if challenge_title_details.challenge_image
#                     else ""
#                 )
#                 challenges_data[i][
#                     "is_limited_time_challenge"
#                 ] = challenge_title_details.is_limited_time_challenge
#                 challenges_data[i]["total_participants"] = (
#                     ParticipantsInPublicCustomGroupChallengesModel.objects.filter(
#                         group_challenge_id=challenges_data[i]["id"]
#                     )
#                     .all()
#                     .count()
#                 )
#                 challenges_data[i]["cash_prize_distribution"] = ""
#                 base_amount = int(challenges_data[i]["price_to_pay"])
#                 if challenges_data[i]["total_participants"] == 1:
#                     total_prize = challenges_data[i]["total_participants"] * base_amount
#                 else:
#                     total_prize = (
#                         challenges_data[i]["total_participants"] * base_amount
#                     ) * 0.9
#                 lowest_amount = 0.5 * total_prize
#                 print(f"lowest_amount {lowest_amount}")
#                 challenges_data[i]["cash_pool"] = total_prize
#                 if challenges_data[i]["total_participants"] == 1:
#                     challenges_data[i]["cash_prize_distribution"] = f"{total_prize}"
#                 elif (
#                     challenges_data[i]["total_participants"] == 2
#                     or challenges_data[i]["total_participants"] == 3
#                 ):
#                     challenges_data[i][
#                         "cash_prize_distribution"
#                     ] = f"{0.8*total_prize} {0.2*total_prize}"
#                 elif challenges_data[i]["total_participants"] <= 10:
#                     challenges_data[i][
#                         "cash_prize_distribution"
#                     ] = f"{0.6*total_prize} {0.25*total_prize} {0.15*total_prize}"
#                 elif challenges_data[i]["total_participants"] > 10:
#                     challenges_data[i][
#                         "cash_prize_distribution"
#                     ] = f"{0.5*total_prize} {0.20*total_prize} {0.20*total_prize} {0.1*total_prize} {lowest_amount} {lowest_amount} {lowest_amount}"
#                 challenges_data[i]["total_videos_submitted"] = len(
#                     ParticipantsInPublicCustomGroupChallengesModel.objects.filter(
#                         group_challenge_id=challenges_data[i]["id"],
#                         has_submitted_video=True,
#                     ).all()
#                 )
#                 challenges_data[i]["is_user_participating"] = False
#                 if challenges_data[i]["challenge_date"] > today_date:
#                     challenges_data[i]["is_participation_allowed"] = True
#                 user_ids_queryset = (
#                     ParticipantsInPublicCustomGroupChallengesModel.objects.filter(
#                         group_challenge_id=challenges_data[i]["id"]
#                     ).values_list("user_id", flat=True)
#                 )
#                 print(f"user_ids_queryset {user_ids_queryset}")
#                 challenges_data[i]["all_participants_id"] = user_ids_queryset
#                 if challenges_data[i]["challenge_date"] < today_date:
#                     challenges_data[i]["is_past_competition"] = True
#                 if challenges_data[i]["challenge_date"] > today_date:
#                     challenges_data[i]["is_future_competition"] = True
#                 challenges_data[i]["challenge_rules"] = (
#                     RulesOfGroupChallengeModel.objects.values().filter().all()
#                 )
#                 for j in range(0, len(challenges_data[i]["challenge_rules"])):
#                     challenges_data[i]["challenge_rules"][j].pop("created_at")
#                     challenges_data[i]["challenge_rules"][j].pop("updated_at")
#                 challenges_data[i]["challenge_guidelines"] = (
#                     GuidelinesOfGroupChallengeModel.objects.values().filter().all()
#                 )
#                 for j in range(0, len(challenges_data[i]["challenge_guidelines"])):
#                     challenges_data[i]["challenge_guidelines"][j].pop("created_at")
#                     challenges_data[i]["challenge_guidelines"][j].pop("updated_at")
#                     challenges_data[i]["challenge_guidelines"][j].pop(
#                         "group_challenge_id"
#                     )
#                 challenges_data[i]["has_user_submitted_video"] = False
#                 challenges_data[i]["challenge_video"] = ""
#                 print(challenges_data[i]["id"])
#                 is_user_participant = (
#                     ParticipantsInPublicCustomGroupChallengesModel.objects.filter(
#                         user_id=user_id, group_challenge_id=challenges_data[i]["id"]
#                     ).first()
#                 )
#                 if is_user_participant is not None:
#                     challenges_data[i]["is_user_participating"] = True
#                     challenges_data[i][
#                         "has_user_submitted_video"
#                     ] = is_user_participant.has_submitted_video
#                     if challenges_data[i]["has_user_submitted_video"]:
#                         challenges_data[i]["challenge_video"] = str(
#                             is_user_participant.challenge_video.path
#                         ).split("/")[
#                             len(
#                                 str(is_user_participant.challenge_video.path).split("/")
#                             )
#                             - 1
#                         ]
#                 if is_user_participant is not None:
#                     challenges_data[i]["is_user_participating"] = True
#             challenges_data = sorted(
#                 challenges_data, key=lambda d: d["created_at"], reverse=True
#             )
#             if sort_by is not None:
#                 if sort_by == "Latest to Oldest":
#                     challenges_data = sorted(
#                         challenges_data, key=lambda d: d["created_at"], reverse=True
#                     )
#                 elif sort_by == "Oldest to Latest":
#                     challenges_data = sorted(
#                         challenges_data, key=lambda d: d["created_at"]
#                     )
#                 elif sort_by == "Max to min participants":
#                     challenges_data = sorted(
#                         challenges_data,
#                         key=lambda d: d["total_participants"],
#                         reverse=True,
#                     )
#                 elif sort_by == "Min to max participants":
#                     challenges_data = sorted(
#                         challenges_data, key=lambda d: d["total_participants"]
#                     )
#             for i in range(0, len(challenges_data)):
#                 challenges_data[i].pop("created_at")
#                 challenges_data[i].pop("updated_at")
#             does_today_data_exists = LogsOfPagesOfUserModel.objects.filter(
#                 user_id=user_id
#             ).last()
#             if does_today_data_exists is None:
#                 new_data = LogsOfPagesOfUserModel.objects.create(
#                     user_id=user_id, group_challenges_page=1
#                 )
#                 new_data.save()
#             else:
#                 does_today_data_exists.group_challenges_page = (
#                     does_today_data_exists.group_challenges_page + 1
#                 )
#                 does_today_data_exists.save()
#             return Response(
#                 ResponseData.success(
#                     challenges_data, "Challenges fetched successfully"
#                 ),
#                 status=status.HTTP_201_CREATED,
#             )
#         return Response(
#             ResponseData.error(serializer.errors),
#             status=status.HTTP_400_BAD_REQUEST,
#         )
#     except Exception as exception:
#         return Response(
#             ResponseData.error(str(exception)),
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         )


# @api_view(["POST"])
# @authentication_classes([ApiKeyAuthentication])
# def get_all_private_custom_group_challenges(request):
#     """Function to get private group challenges based on date"""
#     try:
#         data = request.data
#         print(f"data {data}")
#         user = UserModel.objects.filter(
#             id=request.data["user_id"], is_active=True
#         ).first()
#         if not user:
#             return Response(
#                 ResponseData.error("User id is invalid"),
#                 status=status.HTTP_200_OK,
#             )
#         serializer = GetGroupChallengesSerializer(data=data)
#         if serializer.is_valid():
#             user_id = serializer.data["user_id"]
#             is_my_challenges = (
#                 serializer.data["is_my_challenges"]
#                 if (serializer.data["is_my_challenges"] == True)
#                 else None
#             )
#             is_finished = (
#                 serializer.data["is_finished"]
#                 if (serializer.data["is_finished"] == True)
#                 else None
#             )
#             is_ongoing = (
#                 serializer.data["is_ongoing"]
#                 if (serializer.data["is_ongoing"] == True)
#                 else None
#             )
#             is_upcoming = (
#                 serializer.data["is_upcoming"]
#                 if (serializer.data["is_upcoming"] == True)
#                 else None
#             )
#             sort_by = serializer.data["sort_by"]
#             page_number = int(
#                 serializer.data["page_no"] if "page_no" in request.data else 0
#             )
#             page_size_param = int(
#                 serializer.data["page_size"] if "page_size" in request.data else 0
#             )
#             page_no = page_number
#             page_size = page_size_param
#             start = (page_no - 1) * page_size
#             end = page_no * page_size
#             today_date = datetime.now().date()
#             if is_my_challenges is not None and is_finished is None:
#                 group_challenge_ids = (
#                     ParticipantsInPrivateCustomGroupChallengesModel.objects.filter(
#                         user_id=user_id, is_active=True
#                     ).values_list("group_challenge_id", flat=True)
#                 )
#                 challenges_data = (
#                     PrivateCustomGroupChallengesModel.objects.values()
#                     .filter(id__in=group_challenge_ids)
#                     .all()[start:end]
#                 )
#             elif is_my_challenges is not None and is_finished is not None:
#                 group_challenge_ids = (
#                     ParticipantsInPrivateCustomGroupChallengesModel.objects.filter(
#                         user_id=user_id, is_active=True
#                     ).values_list("group_challenge_id", flat=True)
#                 )
#                 challenges_data = (
#                     PrivateCustomGroupChallengesModel.objects.values()
#                     .filter(id__in=group_challenge_ids, challenge_date__lt=today_date)
#                     .all()[start:end]
#                 )
#             if is_finished is not None:
#                 challenges_data = (
#                     PrivateCustomGroupChallengesModel.objects.values()
#                     .filter(challenge_date__lt=today_date)
#                     .all()[start:end]
#                 )
#             elif is_ongoing is not None:
#                 challenges_data = (
#                     PrivateCustomGroupChallengesModel.objects.values()
#                     .filter(
#                         challenge_date__lte=today_date, challenge_date__gte=today_date
#                     )
#                     .all()[start:end]
#                 )
#             elif is_upcoming is not None:
#                 challenges_data = (
#                     PrivateCustomGroupChallengesModel.objects.values()
#                     .filter(challenge_date__gt=today_date)
#                     .all()[start:end]
#                 )
#             else:
#                 challenges_data = (
#                     PrivateCustomGroupChallengesModel.objects.values()
#                     .filter()
#                     .all()[start:end]
#                 )
#             if len(challenges_data) == 0:
#                 return Response(
#                     ResponseData.success([], "No group challenge found"),
#                     status=status.HTTP_201_CREATED,
#                 )
#             for i in range(0, len(challenges_data)):
#                 challenge_title_details = (
#                     PublicCustomGroupChallengesTitleModel.objects.filter(
#                         id=challenges_data[i]["challenge_details_id"]
#                     ).last()
#                 )
#                 challenges_data[i]["suggested_workout"] = (
#                     PrivateCustomGroupChallengesModel(**challenges_data[i])
#                     .challenge_details.suggested_workout.values("mainTitle", "id")
#                     .all()
#                 )
#                 challenges_data[i][
#                     "is_user_rating_between_this_competition_rating"
#                 ] = False
#                 challenges_data[i]["is_past_competition"] = False
#                 challenges_data[i]["is_future_competition"] = False
#                 challenges_data[i]["is_for_free_trial"] = True
#                 challenges_data[i]["is_bidding_challenge"] = True
#                 challenges_data[i]["host_user_name"] = (
#                     UserModel.objects.filter(
#                         id=challenges_data[i]["host_user_id"], is_active=True
#                     )
#                     .get()
#                     .full_name
#                 )
#                 challenges_data[i][
#                     "challenge_name"
#                 ] = challenge_title_details.challenge_title
#                 challenges_data[i]["challenge_image"] = (
#                     os.path.basename(challenge_title_details.challenge_image.path)
#                     if challenge_title_details.challenge_image
#                     else ""
#                 )
#                 challenges_data[i][
#                     "is_limited_time_challenge"
#                 ] = challenge_title_details.is_limited_time_challenge
#                 challenges_data[i]["total_participants"] = (
#                     ParticipantsInPrivateCustomGroupChallengesModel.objects.filter(
#                         group_challenge_id=challenges_data[i]["id"], is_active=True
#                     )
#                     .all()
#                     .count()
#                 )
#                 challenges_data[i]["paid_participants"] = (
#                     PrivateCustomGroupChallengesPaymentModel.objects.filter(
#                         group_challenge_id=challenges_data[i]["id"]
#                     )
#                     .all()
#                     .count()
#                 )
#                 challenges_data[i]["cash_prize_distribution"] = ""
#                 base_amount = int(challenges_data[i]["price_to_pay"])
#                 if challenges_data[i]["total_participants"] == 1:
#                     total_prize = challenges_data[i]["total_participants"] * base_amount
#                 else:
#                     total_prize = (
#                         challenges_data[i]["total_participants"] * base_amount
#                     ) * 0.9
#                 lowest_amount = 0.5 * total_prize
#                 print(f"lowest_amount {lowest_amount}")
#                 challenges_data[i]["cash_pool"] = total_prize
#                 if challenges_data[i]["total_participants"] == 1:
#                     challenges_data[i]["cash_prize_distribution"] = f"{total_prize}"
#                 elif (
#                     challenges_data[i]["total_participants"] == 2
#                     or challenges_data[i]["total_participants"] == 3
#                 ):
#                     challenges_data[i][
#                         "cash_prize_distribution"
#                     ] = f"{0.8*total_prize} {0.2*total_prize}"
#                 elif challenges_data[i]["total_participants"] <= 10:
#                     challenges_data[i][
#                         "cash_prize_distribution"
#                     ] = f"{0.6*total_prize} {0.25*total_prize} {0.15*total_prize}"
#                 elif challenges_data[i]["total_participants"] > 10:
#                     challenges_data[i][
#                         "cash_prize_distribution"
#                     ] = f"{0.5*total_prize} {0.20*total_prize} {0.20*total_prize} {0.1*total_prize} {lowest_amount} {lowest_amount} {lowest_amount}"
#                 challenges_data[i]["total_videos_submitted"] = len(
#                     ParticipantsInPrivateCustomGroupChallengesModel.objects.filter(
#                         group_challenge_id=challenges_data[i]["id"],
#                         is_active=True,
#                         has_submitted_video=True,
#                     ).all()
#                 )
#                 challenges_data[i]["is_user_participating"] = False
#                 challenges_data[i]["is_payment_done"] = False
#                 is_user_invited = (
#                     ParticipantsInPrivateCustomGroupChallengesModel.objects.filter(
#                         group_challenge_id=challenges_data[i]["id"],
#                         is_active=True,
#                         user_id=user_id,
#                     ).last()
#                 )
#                 if (
#                     challenges_data[i]["challenge_date"] > today_date
#                     and is_user_invited is not None
#                 ):
#                     is_payment_done = (
#                         PrivateCustomGroupChallengesPaymentModel.objects.filter(
#                             group_challenge_id=challenges_data[i]["id"], user_id=user_id
#                         ).last()
#                     )
#                     challenges_data[i]["is_user_participating"] = True
#                     if is_payment_done is not None:
#                         challenges_data[i]["is_payment_done"] = True
#                 challenges_data[i]["all_users_details"] = (
#                     UserModel.objects.exclude(pk=user_id)
#                     .values("id", "mobile_number", "full_name")
#                     .all()
#                 )
#                 for j in range(0, len(challenges_data[i]["all_users_details"])):
#                     is_payment_done_by_user = (
#                         PrivateCustomGroupChallengesPaymentModel.objects.filter(
#                             group_challenge_id=challenges_data[i]["id"],
#                             user_id=challenges_data[i]["all_users_details"][j]["id"],
#                         ).last()
#                     )
#                     if is_payment_done_by_user is not None:
#                         challenges_data[i]["all_users_details"][j][
#                             "is_payment_done"
#                         ] = True
#                 user_ids_queryset = (
#                     ParticipantsInPrivateCustomGroupChallengesModel.objects.filter(
#                         group_challenge_id=challenges_data[i]["id"], is_active=True
#                     ).values_list("user_id", flat=True)
#                 )
#                 print(f"user_ids_queryset {user_ids_queryset}")
#                 if user_id == challenges_data[i]["host_user_id"]:
#                     challenges_data[i]["is_payment_done_by_any_participant"] = False
#                     challenges_data[i]["can_host_user_edit"] = False
#                     current_date = datetime.now().date()
#                     difference = challenges_data[i]["challenge_date"] - current_date
#                     if difference >= timedelta(days=2):
#                         challenges_data[i]["can_host_user_edit"] = True
#                     for ids in user_ids_queryset:
#                         if ids != challenges_data[i]["host_user_id"]:
#                             is_payment_done_by_anyone = (
#                                 PrivateCustomGroupChallengesPaymentModel.objects.filter(
#                                     group_challenge_id=challenges_data[i]["id"],
#                                     user_id=ids,
#                                 ).last()
#                             )
#                             if is_payment_done_by_anyone is not None:
#                                 challenges_data[i][
#                                     "is_payment_done_by_any_participant"
#                                 ] = True
#                                 break
#                 challenges_data[i]["all_participants_id"] = user_ids_queryset
#                 if challenges_data[i]["challenge_date"] < today_date:
#                     challenges_data[i]["is_past_competition"] = True
#                 if challenges_data[i]["challenge_date"] > today_date:
#                     challenges_data[i]["is_future_competition"] = True
#                 challenges_data[i]["challenge_rules"] = (
#                     RulesOfGroupChallengeModel.objects.values().filter().all()
#                 )
#                 for j in range(0, len(challenges_data[i]["challenge_rules"])):
#                     challenges_data[i]["challenge_rules"][j].pop("created_at")
#                     challenges_data[i]["challenge_rules"][j].pop("updated_at")
#                 challenges_data[i]["challenge_guidelines"] = (
#                     GuidelinesOfGroupChallengeModel.objects.values().filter().all()
#                 )
#                 for j in range(0, len(challenges_data[i]["challenge_guidelines"])):
#                     challenges_data[i]["challenge_guidelines"][j].pop("created_at")
#                     challenges_data[i]["challenge_guidelines"][j].pop("updated_at")
#                     challenges_data[i]["challenge_guidelines"][j].pop(
#                         "group_challenge_id"
#                     )
#                 challenges_data[i]["has_user_submitted_video"] = False
#                 challenges_data[i]["challenge_video"] = ""
#                 print(challenges_data[i]["id"])
#                 is_user_participant = (
#                     ParticipantsInPrivateCustomGroupChallengesModel.objects.filter(
#                         user_id=user_id,
#                         group_challenge_id=challenges_data[i]["id"],
#                         is_active=True,
#                     ).first()
#                 )
#                 if is_user_participant is not None:
#                     challenges_data[i]["is_user_participating"] = True
#                     challenges_data[i][
#                         "has_user_submitted_video"
#                     ] = is_user_participant.has_submitted_video
#                     if challenges_data[i]["has_user_submitted_video"]:
#                         challenges_data[i]["challenge_video"] = str(
#                             is_user_participant.challenge_video.path
#                         ).split("/")[
#                             len(
#                                 str(is_user_participant.challenge_video.path).split("/")
#                             )
#                             - 1
#                         ]
#                 if is_user_participant is not None:
#                     challenges_data[i]["is_user_participating"] = True
#             challenges_data = sorted(
#                 challenges_data, key=lambda d: d["created_at"], reverse=True
#             )
#             if sort_by is not None:
#                 if sort_by == "Latest to Oldest":
#                     challenges_data = sorted(
#                         challenges_data, key=lambda d: d["created_at"], reverse=True
#                     )
#                 elif sort_by == "Oldest to Latest":
#                     challenges_data = sorted(
#                         challenges_data, key=lambda d: d["created_at"]
#                     )
#                 elif sort_by == "Max to min participants":
#                     challenges_data = sorted(
#                         challenges_data,
#                         key=lambda d: d["total_participants"],
#                         reverse=True,
#                     )
#                 elif sort_by == "Min to max participants":
#                     challenges_data = sorted(
#                         challenges_data, key=lambda d: d["total_participants"]
#                     )
#             for i in range(0, len(challenges_data)):
#                 challenges_data[i].pop("created_at")
#                 challenges_data[i].pop("updated_at")
#             does_today_data_exists = LogsOfPagesOfUserModel.objects.filter(
#                 user_id=user_id
#             ).last()
#             if does_today_data_exists is None:
#                 new_data = LogsOfPagesOfUserModel.objects.create(
#                     user_id=user_id, group_challenges_page=1
#                 )
#                 new_data.save()
#             else:
#                 does_today_data_exists.group_challenges_page = (
#                     does_today_data_exists.group_challenges_page + 1
#                 )
#                 does_today_data_exists.save()
#             return Response(
#                 ResponseData.success(
#                     challenges_data, "Challenges fetched successfully"
#                 ),
#                 status=status.HTTP_201_CREATED,
#             )
#         return Response(
#             ResponseData.error(serializer.errors),
#             status=status.HTTP_400_BAD_REQUEST,
#         )
#     except Exception as exception:
#         return Response(
#             ResponseData.error(str(exception)),
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         )


# @api_view(["POST"])
# @authentication_classes(
#     [
#         ApiKeyAuthentication,
#     ]
# )
# def get_user_group_challenges(request):
#     """Function to get group challenges in which user has participated"""
#     try:
#         data = request.data
#         print(f"data {data}")
#         user = UserModel.objects.filter(
#             id=request.data["user_id"], is_active=True
#         ).first()
#         if not user:
#             return Response(
#                 ResponseData.error("User id is invalid"),
#                 status=status.HTTP_200_OK,
#             )
#         serializer = GetGroupChallengesSerializer(data=data)
#         if serializer.is_valid():
#             print("true")
#             user_id = serializer.data["user_id"]
#             # is_ongoing = serializer.data['is_ongoing']
#             # is_finished = serializer.data['is_finished']
#             sort_by = serializer.data["sort_by"]
#             challenge_type = serializer.data["challenge_type"]
#             page_number = int(
#                 serializer.data["page_no"] if "page_no" in request.data else 0
#             )
#             page_size_param = int(
#                 serializer.data["page_size"] if "page_size" in request.data else 0
#             )
#             page_no = page_number
#             page_size = page_size_param
#             start = (page_no - 1) * page_size
#             end = page_no * page_size
#             if challenge_type == "subscribed":
#                 return get_all_subscribed_users_group_challenges(request)
#             # elif challenge_type == 'free_trial':
#             #     returned_data = get_challenges_data(challenge_type,ParticipantsInGroupChallengesForFreeTrialModel,GroupChallengesForFreeTrialModel,user_id,'group_challenges',start,end)
#             # elif challenge_type == 'bidding':
#             #     returned_data = get_challenges_data(challenge_type,ParticipantsInBiddingGroupChallengesModel,BiddingGroupChallengesModel,user_id,'group_challenges',start,end)
#             # if is_ongoing is not None:
#             #     total_challenges_data = ParticipantsInGroupChallengeModel.objects.values().filter(user_id=user_id,
#             #     group_challenge__challenge_date__lte=today_date,group_challenge__challenge_date__gte=today_date).all()[start:end]
#             # elif is_finished is not None:
#             #     total_challenges_data = ParticipantsInGroupChallengeModel.objects.values().filter(user_id=user_id,
#             #     group_challenge__challenge_date__lt=today_date).all()[start:end]
#             # else:
#             # if is_ongoing is not None:
#             #     challenges_data = GroupChallengesModel.objects.values().filter(id=total_challenges_data[i]["group_challenge_id"],challenge_date__lte=today_date,challenge_date__gte=today_date).get()
#             # elif is_finished is not None:
#             #     challenges_data = GroupChallengesModel.objects.values().filter(id=total_challenges_data[i]["group_challenge_id"],challenge_date__lt=today_date).get()
#             # else:
#             # if(sort_by is not None):
#             #     if(sort_by == 'Latest to Oldest'):
#             #         final_list = sorted(final_list, key=lambda d: d['created_at'],reverse=True)
#             #     elif(sort_by == 'Oldest to Latest'):
#             #         final_list = sorted(final_list, key=lambda d: d['created_at'])
#             #     elif(sort_by == 'Max to min participants'):
#             #         final_list = sorted(final_list, key=lambda d: d['total_participants'],reverse=True)
#             #     elif(sort_by == 'Min to max participants'):
#             #         final_list = sorted(final_list, key=lambda d: d['total_participants'])
#             # for i in range(0,len(final_list)):
#             #     final_list[i].pop('created_at')
#             #     final_list[i].pop('updated_at')
#             # return Response(
#             #            ResponseData.success(
#             #                final_list, "User Challenges fetched successfully"),
#             #            status=status.HTTP_201_CREATED)
#         return Response(
#             ResponseData.error(serializer.errors),
#             status=status.HTTP_400_BAD_REQUEST,
#         )
#     except Exception as exception:
#         return Response(
#             ResponseData.error(str(exception)),
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         )


@api_view(["POST"])
@authentication_classes(
    [
        ApiKeyAuthentication,
    ]
)
def get_all_participants_of_group_challenge(request):
    """Function to get all users participated in group challenge"""
    try:
        data = request.data
        serializer = GetAllParticipantsOfGroupChallengeSerializer(data=data)
        if serializer.is_valid():
            group_challenge_id = serializer.data["group_challenge_id"]
            challenge_type = serializer.data["challenge_type"]
            page_number = int(
                serializer.data["page_no"] if "page_no" in request.data else 0
            )
            page_size_param = int(
                serializer.data["page_size"] if "page_size" in request.data else 0
            )
            page_no = page_number
            page_size = page_size_param
            start = (page_no - 1) * page_size
            end = page_no * page_size
            challenge_data = (
                ParticipantsInGroupChallengesModel.objects.values()
                .filter(
                    challenge_type__type=challenge_type,
                    group_challenge_id=group_challenge_id,
                    hide_from_user=False,
                )
                .all()[start:end]
            )
            if len(challenge_data) == 0:
                return Response(
                    ResponseData.success([], "No participant found"),
                    status=status.HTTP_201_CREATED,
                )
            for i in range(0, len(challenge_data)):
                challenge_data[i]["user_data"] = (
                    UserModel.objects.values()
                    .filter(id=challenge_data[i]["user_id"])
                    .first()
                )
                challenge_data[i].pop("user_id")
                challenge_data[i]["user_data"].pop("updated_at")
                challenge_data[i]["user_data"].pop("created_at")
                challenge_data[i].pop("updated_at")
                challenge_data[i].pop("created_at")
                challenge_data[i].pop("hide_from_user")
                if challenge_data[i]["date_of_submission"] is None:
                    challenge_data[i]["date_of_submission"] = ""
            return Response(
                ResponseData.success(
                    challenge_data, "User details fetched successfully"
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
def add_user_in_group_challenge(request):
    """Function to add user in a group challenge"""
    try:
        data = request.data
        serializer = AddNewUserInGroupChallengeSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            challenge_type = serializer.data["challenge_type"]
            group_challenge_id = serializer.data["group_challenge_id"]
            user = UserModel.objects.filter(id=user_id, is_active=True).first()
            if not user:
                return Response(
                    ResponseData.error("User id is invalid"),
                    status=status.HTTP_200_OK,
                )
            group_challenge = GroupChallengeModel.objects.filter(
                challenge_type__type=challenge_type, id=group_challenge_id
            ).first()
            if not group_challenge:
                return Response(
                    ResponseData.error("Group challenge id is invalid"),
                    status=status.HTTP_200_OK,
                )
            is_user_already_a_participant = (
                ParticipantsInGroupChallengesModel.objects.filter(
                    challenge_type__type=challenge_type,
                    user_id=user_id,
                    group_challenge_id=group_challenge_id,
                    hide_from_user=False,
                ).first()
            )
            if is_user_already_a_participant:
                return Response(
                    ResponseData.error(
                        "You are already a participant in this challenge"
                    ),
                    status=status.HTTP_200_OK,
                )
            challenge_type_data = GroupChallengeTypeModel.objects.filter(
                type=challenge_type
            ).last()
            new_data = ParticipantsInGroupChallengesModel.objects.create(
                user_id=user_id,
                challenge_type_id=challenge_type_data.id,
                group_challenge_id=group_challenge_id,
            )
            new_data.save()
            return Response(
                ResponseData.success_without_data(
                    "New user added in this group challenge successfully"
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
def add_new_public_custom_group_challenge(request):
    """Function to create new custom public group challenge"""
    try:
        data = request.data
        serializer = CreateNewGroupChallengeSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            challenge_details_id = serializer.data["challenge_details_id"]
            payment_id = serializer.data["payment_id"]
            max_participants_allowed = serializer.data["max_participants_allowed"]
            price_to_pay = serializer.data["price_to_pay"]
            challenge_date = serializer.data["challenge_date"]
            challenge_type = serializer.data["challenge_type"]
            user = UserModel.objects.filter(id=user_id, is_active=True).first()
            if not user:
                return Response(
                    ResponseData.error("User id is invalid"),
                    status=status.HTTP_200_OK,
                )
            current_date = datetime.now().date()
            does_challenge_exists = GroupChallengeModel.objects.filter(
                challenge_date__gt=current_date,
                challenge_type__type=challenge_type,
                is_active=True,
                price_to_pay=price_to_pay,
                challenge_details_id=challenge_details_id,
            )
            if does_challenge_exists is not None:
                return Response(
                    ResponseData.error("Same challenge with same price is upcoming."),
                    status=status.HTTP_201_CREATED,
                )
            challenge_type_data = GroupChallengeTypeModel.objects.filter(
                type=challenge_type
            ).last()
            new_challenge = GroupChallengeModel.objects.create(
                user_id=user_id,
                challenge_type_id=challenge_type_data.id,
                challenge_details_id=challenge_details_id,
                challenge_date=challenge_date,
                max_participants_allowed=max_participants_allowed,
                price_to_pay=price_to_pay,
            )
            new_challenge.save()
            new_payment = GroupChallengesPaymentModel.objects.create(
                user_id=user_id,
                payment_id=payment_id,
                challenge_type_id=challenge_type_data.id,
                group_challenge_id=new_challenge.id,
                date_of_payment=datetime.now(),
            )
            new_payment.save()
            add_this_participant = ParticipantsInGroupChallengesModel.objects.create(
                user_id=user_id,
                challenge_type_id=challenge_type_data.id,
                group_challenge_id=new_challenge.id,
            )
            add_this_participant.save()
            return Response(
                ResponseData.success_without_data(
                    "Custom challenge created successfully"
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
def add_new_private_custom_group_challenge(request):
    """Function to create new custom private group challenge"""
    try:
        data = request.data
        print(f"data {data}")
        serializer = CreateNewGroupChallengeSerializer(data=data)
        if serializer.is_valid():
            host_user_id = serializer.data["host_user_id"]
            challenge_details_id = serializer.data["challenge_details_id"]
            payment_id = serializer.data["payment_id"]
            price_to_pay = serializer.data["price_to_pay"]
            challenge_date = serializer.data["challenge_date"]
            challenge_type = serializer.data["challenge_type"]
            participants = serializer.data["participants"]
            is_edit = serializer.data["is_edit"] if "is_edit" in request.data else False
            user = UserModel.objects.filter(id=host_user_id, is_active=True).first()
            if not user:
                return Response(
                    ResponseData.error("User id is invalid"),
                    status=status.HTTP_200_OK,
                )
            current_date = datetime.now().date()
            challenge_type_data = GroupChallengeTypeModel.objects.filter(
                type=challenge_type
            ).last()
            if is_edit:
                challenge_details = GroupChallengeModel.objects.filter(
                    challenge_type__type=challenge_type,
                    is_active=True,
                    id=challenge_details_id,
                ).last()
                before_all_participants = (
                    ParticipantsInGroupChallengesModel.objects.filter(
                        challenge_type__type=challenge_type,
                        is_active=True,
                        group_challenge_id=challenge_details_id,
                    ).all()
                )
                for participant in before_all_participants:
                    if (
                        participant.user_id not in participants
                        and participant.user_id != challenge_details.host_user_id
                    ):
                        participant.is_active = False
                        participant.save()
                    for par in participants:
                        each_participant = (
                            ParticipantsInGroupChallengesModel.objects.filter(
                                is_active=True,
                                user_id=par,
                                group_challenge_id=challenge_details_id,
                            ).last()
                        )
                        if each_participant is None:
                            new_participant = (
                                ParticipantsInGroupChallengesModel.objects.create(
                                    user_id=par,
                                    challenge_type_id=challenge_type_data.id,
                                    group_challenge_id=challenge_details_id,
                                )
                            )
                            new_participant.save()
                return Response(
                    ResponseData.success_without_data(
                        "Private challenge updated successfully"
                    ),
                    status=status.HTTP_201_CREATED,
                )
            else:
                does_challenge_exists = GroupChallengeModel.objects.filter(
                    challenge_date__gt=current_date,
                    challenge_type__type=challenge_type,
                    is_active=True,
                    price_to_pay=price_to_pay,
                    challenge_details_id=challenge_details_id,
                )
                print(f"does_challenge_exists {does_challenge_exists}")
                if len(does_challenge_exists) > 0:
                    return Response(
                        ResponseData.error(
                            "Same challenge with same price is upcoming."
                        ),
                        status=status.HTTP_201_CREATED,
                    )
                new_challenge = GroupChallengeModel.objects.create(
                    challenge_date=challenge_date,
                    price_to_pay=price_to_pay,
                    challenge_details_id=challenge_details_id,
                    host_user_id=host_user_id,
                    challenge_type_id=challenge_type_data.id,
                )
                new_challenge.save()
                final_data = []
                for i in participants:
                    final_data.append(
                        ParticipantsInGroupChallengesModel(
                            user_id=i,
                            challenge_type_id=challenge_type_data.id,
                            group_challenge=new_challenge.id,
                        )
                    )
                ParticipantsInGroupChallengesModel.objects.bulk_create(final_data)
                new_payment = GroupChallengesPaymentModel.objects.create(
                    user_id=host_user_id,
                    payment_id=payment_id,
                    challenge_type_id=challenge_type_data.id,
                    group_challenge_id=new_challenge.id,
                    date_of_payment=datetime.now(),
                )
                new_payment.save()
                return Response(
                    ResponseData.success_without_data(
                        "Private challenge created successfully"
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


def getChallengeAndParticipantData(
    challenge_id,
    user_id,
    app_label_for_challenge,
    model_name_for_challenge,
    app_label_for_participant,
    model_name_for_participant,
):
    ModelClassForChallenge = apps.get_model(
        app_label_for_challenge, model_name_for_challenge
    )
    group_challenge = ModelClassForChallenge.objects.filter(id=challenge_id).first()
    if not group_challenge:
        return Response(
            ResponseData.error("Group challenge id is invalid"),
            status=status.HTTP_200_OK,
        )
    ModelClassForParticipant = apps.get_model(
        app_label_for_participant, model_name_for_participant
    )
    user_challenge_data = ModelClassForParticipant.objects.filter(
        user_id=user_id, group_challenge_id=challenge_id, hide_from_user=False
    ).all()
    if len(user_challenge_data) == 0:
        return Response(
            ResponseData.error(
                "You are not a participant yet. Please participate first."
            ),
            status=status.HTTP_200_OK,
        )
    return group_challenge,user_challenge_data


def has_submitted_video_for_user(user_id, challenge_type):
    # Query all records for the user_id
    records = ParticipantsInGroupChallengesModel.objects.filter(
        user_id=user_id, challenge_type__type=challenge_type
    )

    # Check if all records have has_submitted_video as True
    all_submitted = all(record.has_submitted_video for record in records)

    return all_submitted


@shared_task
def save_video_file(user_id, group_challenge_id, current_datetime, challenge_type, video_file):
    print("dvdvdfvdfvdfv")
    fs = FileSystemStorage(location="static/")
    fs.save(f"{user_id}_{group_challenge_id}_{current_datetime}_{challenge_type}.mp4", video_file)

@api_view(["POST"])
@authentication_classes(
    [
        ApiKeyAuthentication,
    ]
)
def upload_video_for_group_challenge(request):
    """Function to upload challenge video of a user"""
    try:
        data = request.data
        print(f"data {data}")
        serializer = UploadVideoOfUserGroupChallengeSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            total_number = serializer.data['total_number']
            group_challenge_id = serializer.data["group_challenge_id"]
            video_file = request.FILES["video_file"]
            is_updated_file = request.data["is_updated_file"]
            user = UserModel.objects.filter(id=user_id, is_active=True).first()
            if not user:
                return Response(
                    ResponseData.error("User id is invalid"),
                    status=status.HTTP_200_OK,
                )
            app_label_for_challenge = "group_challenges"
            app_label_for_participant = "group_challenges"
            model_name_for_challenge = "GroupChallengeModel"
            model_name_for_participant = "ParticipantsInGroupChallengesModel"
            group_challenge, user_challenge_data = getChallengeAndParticipantData(
                group_challenge_id,
                user_id,
                app_label_for_challenge,
                model_name_for_challenge,
                app_label_for_participant,
                model_name_for_participant,
            )
            print(f"group_challenge {group_challenge.challenge_type.type}")
            challenge_type = group_challenge.challenge_type.type
            if is_updated_file is True:
                print(
                    f"user_challenge_data.challenge_video {user_challenge_data[0].challenge_video}"
                )
                fs = FileSystemStorage(location="static/")
                fs.delete(str(user_challenge_data[0].challenge_video).split("/")[1])
            currentDateTime = datetime.now()
            user_challenge_data[0].challenge_video = (
                f"static/{user.id}_{group_challenge_id}_{currentDateTime}_{challenge_type}.mp4"
            )
            user_challenge_data[0].has_submitted_video = True
            user_challenge_data[0].save()
            if video_file != "" or video_file is not None:
                fs = FileSystemStorage(location="static/")
                fs.save(f"{user_id}_{group_challenge_id}_{currentDateTime}_{challenge_type}.mp4", video_file)
                print("save_video_called")
            if challenge_type == "free_trial":
                if has_submitted_video_for_user(user_id, challenge_type):
                    current_date = datetime.now().date()
                    upcoming_30th_date = datetime(
                        current_date.year, current_date.month, 30
                    )
                    upcoming_free_trial_challenge = GroupChallengeModel.objects.filter(
                        challenge_type__type=challenge_type,
                        challenge_date=upcoming_30th_date,
                    )
                    challenge_type_data = GroupChallengeTypeModel.objects.filter(
                        type=challenge_type
                    ).last()
                    make_user_participant = (
                        ParticipantsInGroupChallengesModel.objects.create(
                            user_id=user_id,
                            challenge_type_id=challenge_type_data.id,
                            group_challenge_id=upcoming_free_trial_challenge.id,
                        )
                    )
                    make_user_participant.save()
            challenge_result = ChallengesResultModel.objects.create(
                user_id=user_id,
                group_challenge_id=group_challenge_id,
                total_done=total_number,
                description='',
            )
            challenge_result.save()
            return Response(
                ResponseData.success_without_data("Video uploaded successfully"),
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


# @api_view(["POST"])
# @authentication_classes([ApiKeyAuthentication,])
# def update_user_participation_for_group_challenge(request):
#     """Function to update user particiation for group challenge"""
#     try:
#         data = request.data
#         serializer = UpdateUserParticipationStatusInGroupChallengeSerializer(data=data)
#         if serializer.is_valid():
#             user_id = serializer.data["user_id"]
#             group_challenge_id = serializer.data["group_challenge_id"]
#             want_to_participate = serializer.data['want_to_participate']
#             user = UserModel.objects.filter(id=user_id,is_active=True).first()
#             if not user:
#                    return Response(
#                        ResponseData.error("User id is invalid"),
#                        status=status.HTTP_200_OK,
#                    )
#             group_challenge = GroupChallengesModel.objects.filter(id=group_challenge_id).first()
#             if not group_challenge:
#                    return Response(
#                        ResponseData.error("Group challenge id is invalid"),
#                        status=status.HTTP_200_OK,
#                    )
#             user_challenge_data = ParticipantsInGroupChallengeModel.objects.filter(user_id=user_id,group_challenge_id=group_challenge_id).get()
#             if user_challenge_data is None:
#                 return Response(
#                        ResponseData.error("You are not a participant yet. Please participate first."),
#                        status=status.HTTP_200_OK,
#                    )
#             if want_to_participate == False:
#                 user_challenge_data.hide_from_user = True
#                 user_challenge_data.save()
#             else:
#                 user_challenge_data.hide_from_user = False
#                 user_challenge_data.save()
#             return Response(
#                 ResponseData.success_without_data(
#                     "Status updated successfully"),
#                 status=status.HTTP_201_CREATED,
#             )
#         for error in serializer.errors:
#             print(serializer.errors[error][0])
#         return Response(
#             ResponseData.error(serializer.errors[error][0]),
#             status=status.HTTP_400_BAD_REQUEST,
#         )
#     except Exception as exception:
#         return Response(
#             ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )
