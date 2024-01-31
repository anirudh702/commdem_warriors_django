from datetime import datetime

from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from bidding_contest.models import (
    AnswersOfBiddingContestModel,
    BiddingContestModel,
    BiddingContestPaymentModel,
    ParticipantsInBiddingContestModel,
    QuestionsForBiddingContestModel,
)
from bidding_contest.serializers import (
    AddNewParticipantSerializer,
    GetBiddingContestSerializer,
    UpdateParticipantDetailsSerializer,
)
from commdem_warriors_backend.authenticators import ApiKeyAuthentication
from group_challenges.models import GroupChallengeModel
from response import Response as ResponseData
from user.models import UserModel

# Create your views here.


@api_view(["POST"])
@authentication_classes([ApiKeyAuthentication])
def get_bidding_contest_details(request):
    """Function to get details of bidding contest"""
    try:
        data = request.data
        print(f"data {request.data}")
        user = UserModel.objects.filter(
            id=request.data["user_id"], is_active=True
        ).first()
        if not user:
            return Response(
                ResponseData.error("User id is invalid"),
                status=status.HTTP_200_OK,
            )
        serializer = GetBiddingContestSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            challenge_id = serializer.data["challenge_id"]
            bidding_contest_data = (
                BiddingContestModel.objects.values()
                .filter(group_challenge_id=challenge_id, is_active=True)
                .all()
            )
            for i in range(0, len(bidding_contest_data)):
                bidding_contest_data[i]["has_user_placed_bid"] = False
                group_challenge_details = GroupChallengeModel.objects.filter(
                    id=bidding_contest_data[i]["group_challenge_id"]
                ).last()
                challenge_date = (
                    group_challenge_details.challenge_date
                )  # Replace 'instance' with your model instance
                current_date = datetime.now().date()
                days_difference = (challenge_date - current_date).days
                # Define the threshold in days
                threshold_days = 2
                # Check if bidding is allowed
                bidding_contest_data[i]["is_bid_allowed_now"] = (
                    0 < days_difference <= threshold_days
                )
                is_payment_done = BiddingContestPaymentModel.objects.filter(
                    bidding_contest_id=bidding_contest_data[i]["id"], user_id=user_id
                ).last()
                if is_payment_done is not None:
                    bidding_contest_data[i]["has_user_placed_bid"] = True
                bidding_contest_data[i]["questions"] = (
                    QuestionsForBiddingContestModel.objects.values()
                    .filter(
                        bidding_contest_id=bidding_contest_data[i]["id"],
                        is_active=True,
                    )
                    .all()
                )
                bidding_contest_data[i]["bids_placed"] = (
                    ParticipantsInBiddingContestModel.objects.values()
                    .filter(
                        bidding_contest_id=bidding_contest_data[i]["id"],
                        is_active=True,
                    )
                    .count()
                )
                for j in range(0, len(bidding_contest_data[i]["questions"])):
                    answer_data = AnswersOfBiddingContestModel.objects.filter(
                        bidding_contest_id=bidding_contest_data[i]["id"],
                        user_id=user_id,
                        question_id=bidding_contest_data[i]["questions"][j]["id"],
                    ).last()
                    print(f"answer_data {answer_data}")
                    if answer_data is not None:
                        if (
                            bidding_contest_data[i]["questions"][j]["title"]
                            == "Select top 3 participants in order"
                        ):
                            final_answer = ""
                            for k in answer_data.answer.strip(",").split(","):
                                sub_user_id = int(k)
                                user_full_name = (
                                    UserModel.objects.filter(
                                        id=sub_user_id, is_active=True
                                    )
                                    .last()
                                    .full_name
                                )
                                final_answer += f"{k}-{user_full_name},"
                            final_answer = final_answer.strip(",")
                            bidding_contest_data[i]["questions"][j][
                                "answer"
                            ] = final_answer
                        else:
                            bidding_contest_data[i]["questions"][j][
                                "answer"
                            ] = answer_data.answer
                if bidding_contest_data[i]["bids_placed"] == 1:
                    total_prize = (
                        bidding_contest_data[i]["bids_placed"]
                        * bidding_contest_data[i]["bid_price"]
                    )
                else:
                    total_prize = (
                        bidding_contest_data[i]["bids_placed"]
                        * bidding_contest_data[i]["bid_price"]
                    ) * 0.9
                lowest_amount = 0.5 * bidding_contest_data[i]["bid_price"]
                print(f"lowest_amount {lowest_amount}")
                bidding_contest_data[i]["cash_pool"] = total_prize
                if (
                    bidding_contest_data[i]["bids_placed"] == 1
                    or bidding_contest_data[i]["bids_placed"] == 2
                ):
                    bidding_contest_data[i][
                        "cash_prize_distribution"
                    ] = f"{total_prize}"
                elif bidding_contest_data[i]["bids_placed"] == 3:
                    bidding_contest_data[i][
                        "cash_prize_distribution"
                    ] = f"{0.7*total_prize} {0.2*total_prize} {0.1*total_prize}"
                elif bidding_contest_data[i]["bids_placed"] > 3:
                    total_prize = (total_prize) - (
                        (bidding_contest_data[i]["bids_placed"] - 3) * lowest_amount
                    )
                    bidding_contest_data[i][
                        "cash_prize_distribution"
                    ] = f"{0.7*total_prize} {0.2*total_prize} {0.1*total_prize} {lowest_amount}"  # noqa: E501
                    bidding_contest_data[i]["questions"][j].pop("created_at")
                    bidding_contest_data[i]["questions"][j].pop("updated_at")
            for i in range(0, len(bidding_contest_data)):
                bidding_contest_data[i].pop("created_at")
                bidding_contest_data[i].pop("updated_at")
            return Response(
                ResponseData.success(
                    bidding_contest_data, "Contest data fetched successfully"
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
def add_participant_in_bidding_contest(request):
    """Function to add new participant in bidding contest"""
    try:
        data = request.data
        print(data)
        serializer = AddNewParticipantSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            payment_id = serializer.data["payment_id"]
            answers = serializer.data["answers"]
            bidding_contest_id = serializer.data["bidding_contest_id"]
            date_of_payment = str(serializer.data["date_of_payment"]).split(" ")[0]
            bidding_contest_details = BiddingContestModel.objects.get(
                id=bidding_contest_id,
            )
            if (
                bidding_contest_details.max_bids_allowed
                == bidding_contest_details.bids_placed
            ):
                bidding_contest_details.max_bids_allowed = (
                    bidding_contest_details.max_bids_allowed + 1
                )
                bidding_contest_details.bids_placed = (
                    bidding_contest_details.bids_placed + 1
                )
                print(bidding_contest_details.max_bids_allowed)
                bidding_contest_details.save()
            new_payment_record = BiddingContestPaymentModel.objects.create(
                user_id=user_id,
                payment_id=payment_id,
                bidding_contest_id=bidding_contest_id,
                date_of_payment=date_of_payment,
            )
            new_payment_record.save()
            new_data = ParticipantsInBiddingContestModel.objects.create(
                user_id=user_id, bidding_contest_id=bidding_contest_id
            )
            new_data.save()
            final_data = []
            for i, obj in enumerate(answers):
                question_id = obj["question_id"]
                answer = obj["answer"]
                final_data.append(
                    AnswersOfBiddingContestModel(
                        answer=answer, user_id=user_id, question_id=question_id
                    )
                )
            AnswersOfBiddingContestModel.objects.bulk_create(final_data)
            return Response(
                ResponseData.success_without_data(
                    "You are added in this contest successfully"
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
def update_participant_details_in_bidding_contest(request):
    """Function to update participant details in bidding contest"""
    try:
        data = request.data
        print(data)
        serializer = UpdateParticipantDetailsSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            answers = serializer.data["answers"]
            bidding_contest_id = serializer.data["bidding_contest_id"]
            for i, obj in enumerate(answers):
                question_id = obj["question_id"]
                answer = obj["answer"]
                get_answer_details = AnswersOfBiddingContestModel.objects.get(
                    bidding_contest_id=bidding_contest_id,
                    user_id=user_id,
                    question_id=question_id,
                )
                print(f" get_answer_details {get_answer_details}")
                get_answer_details.answer = answer
                get_answer_details.save()
            return Response(
                ResponseData.success_without_data("Details updated successfully"),
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
