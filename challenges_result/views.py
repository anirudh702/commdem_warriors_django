from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from challenges_result.models import ChallengesResultModel
from challenges_result.serializers import (
    AddChallengesResultSerializer,
    GetChallengesResultOfUserSerializer,
    GetChallengesResultSerializer,
)
from commdem_warriors_backend.authenticators import ApiKeyAuthentication
from group_challenges.models import (
    GroupChallengeModel,
    GroupChallengeTypeModel,
    ParticipantsInGroupChallengesModel,
)
from response import Response as ResponseData
from user.models import UserModel

# Create your views here.


@api_view(["POST"])
@authentication_classes(
    [
        ApiKeyAuthentication,
    ]
)
def add_challenges_result(request):
    """Function to add new challenges_result details"""
    try:
        data = request.data
        serializer = AddChallengesResultSerializer(data=data)
        if serializer.is_valid():
            data_exists = ChallengesResultModel.objects.filter(
                competition_id=serializer["competition_id"]
            ).first()
            if data_exists:
                return Response(
                    ResponseData.error(
                        "ChallengesResult with these details already exists"
                    ),
                    status=status.HTTP_200_OK,
                )
            new_challenges_result = ChallengesResultModel.objects.create(
                user_id=serializer["user_id"],
                competition_id=serializer["competition_id"],
                total_done=serializer["total_done"],
                description=serializer["description"],
                prize_money=serializer["prize_money"],
            )
            new_challenges_result.save()
            return Response(
                ResponseData.success_without_data(
                    "Challenges Result added successfully"
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
def get_challenges_result_by_id(request):
    """Function to get a challenges_result based on id"""
    try:
        data = request.data
        print(data)
        serializer = GetChallengesResultSerializer(data=data)
        if serializer.is_valid():
            group_challenge_id = serializer.data["group_challenge_id"]
            search_param = (
                data["search_param"] if "search_param" in request.data else ""
            )
            is_id_valid = ChallengesResultModel.objects.filter(
                group_challenge_id=group_challenge_id
            ).first()
            if not is_id_valid:
                return Response(
                    ResponseData.error("ChallengesResult id is invalid"),
                    status=status.HTTP_200_OK,
                )
            challenges_result_data = (
                ChallengesResultModel.objects.values()
                .filter(group_challenge_id=group_challenge_id)
                .filter(
                    Q(user__full_name__icontains=search_param)
                    | Q(user__mobile_number__icontains=search_param)
                    | Q(user__full_name__icontains=search_param)
                    | Q(
                        user__userlocationdetailsmodel__city_name__icontains=search_param
                    )
                )
                if search_param != ""
                else ChallengesResultModel.objects.values().filter(
                    group_challenge_id=group_challenge_id
                )
            )
            for i in range(0, len(challenges_result_data)):
                challenges_result_data[i]["fullname"] = (
                    UserModel.objects.filter(
                        id=challenges_result_data[i]["user_id"], is_active=True
                    )
                    .first()
                    .full_name
                )
                challenges_data = GroupChallengeModel.objects.filter(
                    id=group_challenge_id
                ).first()
                if challenges_data is not None:
                    challenges_result_data[i][
                        "is_limited_time_challenge"
                    ] = challenges_data.is_limited_time_challenge
                    challenges_result_data[i][
                        "challenge_type"
                    ] = challenges_data.challenge_type.type
                challenges_video_data = (
                    ParticipantsInGroupChallengesModel.objects.values()
                    .filter(
                        user_id=challenges_result_data[i]["user_id"],
                        group_challenge_id=challenges_result_data[i][
                            "group_challenge_id"
                        ],
                    )
                    .first()
                )
                if challenges_video_data is not None:
                    challenges_result_data[i]["video_file"] = challenges_video_data[
                        "challenge_video"
                    ]
                challenges_result_data[i].pop("created_at")
                challenges_result_data[i].pop("updated_at")
            is_rank_added = ChallengesResultModel.objects.values().filter(
                group_challenge_id=group_challenge_id, rank=0
            )
            if is_rank_added is not None:
                challenges_result_data = sorted(
                    challenges_result_data, key=lambda x: x["total_done"], reverse=True
                )
                for rank, item in enumerate(challenges_result_data, start=1):
                    print(f"sdvdsvsvsdv {item['id']}")
                    print(f"sdvsdvsdv {item['rank']}")
                    print(f"svsvsdvsv {item}")
                    item["rank"] = rank
                    instance = ChallengesResultModel.objects.get(pk=item["id"])
                    instance.rank = rank
                    instance.save()
            return Response(
                ResponseData.success(
                    challenges_result_data,
                    "ChallengesResult details fetched successfully",
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
def get_all_challenges_result_of_user(request):
    """Function to get all challenges_result of a user"""
    try:
        data = request.data
        print(f"data {data}")
        serializer = GetChallengesResultOfUserSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            challenge_type = serializer.data["challenge_type"]
            sort_by = serializer.data["sort_by"]
            challenge_date = serializer.data["challenge_date"]
            is_user_id_valid = UserModel.objects.filter(
                id=user_id, is_active=True
            ).last()
            if not is_user_id_valid:
                return Response(
                    ResponseData.error("User id is invalid"),
                    status=status.HTTP_200_OK,
                )
            challenges_result_details = ChallengesResultModel.objects.values().filter(
                user_id=user_id
            )
            if challenge_type is not None:
                challenge_type_detail = GroupChallengeTypeModel.objects.filter(
                    type=challenge_type
                ).last()
                challenges_result_details = challenges_result_details.filter(
                    group_challenge__challenge_type_id=challenge_type_detail.id
                )
            if challenge_date is not None:
                challenges_result_details = challenges_result_details.filter(
                    group_challenge__challenge_date=challenge_date
                )
            challenges_result_details = list(challenges_result_details.all())
            # if challenge_type is None and challenge_date is None:
            #     challenges_result_details = list(
            #         ChallengesResultModel.objects.values().filter(user_id=user_id).all()  # noqa: E501
            #     )
            # elif challenge_type is None and challenge_date is not None:
            #     challenges_result_details = list(
            #         ChallengesResultModel.objects.values()
            #         .filter(
            #             user_id=user_id, group_challenge__challenge_date=challenge_date  # noqa: E501
            #         )
            #         .all()
            #     )
            # elif challenge_type is not None and challenge_date is not None:
            #     challenge_type_detail = GroupChallengeTypeModel.objects.filter(
            #         type=challenge_type
            #     ).last()
            #     challenges_result_details = list(
            #         ChallengesResultModel.objects.values()
            #         .filter(
            #             user_id=user_id,
            #             group_challenge__challenge_type_id=challenge_type_detail.id,
            #             group_challenge__challenge_date=challenge_date,
            #         )
            #         .all()
            #     )
            # elif challenge_type is not None and challenge_date is None:
            #     challenge_type_detail = GroupChallengeTypeModel.objects.filter(
            #         type=challenge_type
            #     ).last()
            #     challenges_result_details = list(
            #         ChallengesResultModel.objects.values()
            #         .filter(
            #             user_id=user_id,
            #             group_challenge__challenge_type_id=challenge_type_detail.id,
            #         )
            #         .all()
            #     )
            # print(f"challenges_result_details {challenges_result_details}")
            final_data = []
            for i in range(0, len(challenges_result_details)):
                workoutVideoData = ParticipantsInGroupChallengesModel.objects.filter(
                    user_id=user_id,
                    has_submitted_video=True,
                    group_challenge_id=challenges_result_details[i][
                        "group_challenge_id"
                    ],
                ).last()
                if workoutVideoData is not None:
                    mapData = {}
                    mapData["rank"] = challenges_result_details[i]["rank"]
                    mapData["prize_money"] = challenges_result_details[i]["prize_money"]
                    challengeData = GroupChallengeModel.objects.filter(
                        id=challenges_result_details[i]["group_challenge_id"]
                    ).last()
                    if challengeData is not None:
                        mapData["competition_title"] = challengeData.challenge_title
                        mapData["competition_type"] = challengeData.challenge_type.type
                        mapData["competition_date"] = challengeData.challenge_date
                        mapData["workout_video_url"] = ""
                        if workoutVideoData.challenge_video is not None:
                            mapData["workout_video_url"] = str(
                                workoutVideoData.challenge_video.path
                            ).split("/")[
                                len(
                                    str(workoutVideoData.challenge_video.path).split(
                                        "/"
                                    )
                                )
                                - 1
                            ]
                    final_data.append(mapData)
            if sort_by is not None and sort_by != "":
                if sort_by == "Latest to Oldest":
                    final_data = sorted(
                        final_data, key=lambda d: d["competition_date"], reverse=True
                    )
                elif sort_by == "Oldest to Latest":
                    final_data = sorted(final_data, key=lambda d: d["competition_date"])
                elif sort_by == "top to bottom rank":
                    final_data = sorted(final_data, key=lambda d: d["rank"])
                elif sort_by == "bottom to top rank":
                    final_data = sorted(
                        final_data, key=lambda d: d["rank"], reverse=True
                    )
                elif sort_by == "max to min prize":
                    final_data = sorted(
                        final_data, key=lambda d: d["prize_money"], reverse=True
                    )
                elif sort_by == "min to max prize":
                    final_data = sorted(final_data, key=lambda d: d["prize_money"])
            return Response(
                ResponseData.success(
                    final_data,
                    "ChallengesResult details fetched successfully"
                    if final_data != []
                    else "No Data Found",
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
def delete_challenges_result_by_id(request):
    """Function to delete a challenges_result based on id"""
    try:
        data = request.data
        serializer = GetChallengesResultSerializer(data=data)
        if serializer.is_valid():
            challenges_result_id = serializer.data["id"]
            is_id_valid = ChallengesResultModel.objects.filter(
                id=challenges_result_id
            ).first()
            if not is_id_valid:
                return Response(
                    ResponseData.error("challenges_result id is invalid"),
                    status=status.HTTP_200_OK,
                )
            (
                ChallengesResultModel.objects.values()
                .filter(id=challenges_result_id)
                .delete()
            )
            return Response(
                ResponseData.success_without_data(
                    "ChallengesResult of this id deleted successfully"
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
def delete_all_challenges_result(request):
    """Function to delete all challenges_result"""
    try:
        data = request.data
        serializer = GetChallengesResultSerializer(data=data)
        if serializer.is_valid():
            (ChallengesResultModel.objects.values().filter().delete())
            return Response(
                ResponseData.success_without_data(
                    "All challenges_result deleted successfully"
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
def update_challenges_result(request):
    """Function to update challenges_result details"""
    try:
        data = request.data
        serializer = AddChallengesResultSerializer(data=data)
        if serializer.is_valid():
            challenges_result_id = serializer.data["id"]

            challenges_result_data = ChallengesResultModel.objects.filter(
                id=challenges_result_id
            ).first()
            if not challenges_result_data:
                return Response(
                    ResponseData.error("ChallengesResult id is invalid."),
                    status=status.HTTP_200_OK,
                )
            if "image" in request.FILES:
                fs = FileSystemStorage(location="static/")
                fs.save(request.FILES["image"].name, request.FILES["image"])

            # if 'image' in request.FILES:
            #   userdata.profile_pic = f"static/{request.FILES['image']}"
            challenges_result_data.save()
            updated_data = list(
                ChallengesResultModel.objects.values().filter(id=challenges_result_id)
            )
            return Response(
                ResponseData.success(
                    updated_data[0]["id"],
                    "ChallengesResult details updated successfully",
                ),
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
