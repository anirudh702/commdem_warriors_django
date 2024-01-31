import requests
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from commdem_warriors_backend.authenticators import ApiKeyAuthentication
from oneToOneChatModule.models import OneToOneChatModel
from questions_before_relationship.models import QuestionsToAskBeforeModel
from response import Response as ResponseData
from user.models import (
    UserAnswerBeforeRelationshipModel,
    UserHealthDetailsModel,
    UserModel,
)


# Create your views here.
@api_view(["POST"])
@authentication_classes(
    [
        ApiKeyAuthentication,
    ]
)
def get_all_questions(request):
    """Function to get all questions to answer before relationship"""
    try:
        data = request.data
        print(f"datadfdfvd {data}")
        user_id = data["user_id"]
        root_user_id = data["root_user_id"]
        questions_data = QuestionsToAskBeforeModel.objects.values().all()
        user = UserModel.objects.filter(id=user_id).first()
        if not user:
            return Response(
                ResponseData.error("User id is invalid"),
                status=status.HTTP_201_CREATED,
            )
        if len(questions_data) == 0:
            return Response(
                ResponseData.success([], "No question found"),
                status=status.HTTP_201_CREATED,
            )
        first_message_time_after_match = OneToOneChatModel.objects.filter(
            (Q(from_user_id=root_user_id) & Q(to_user_id=user_id))
            | (Q(from_user_id=user_id) & Q(to_user_id=root_user_id))
        ).first()
        for i in range(0, len(questions_data)):
            questions_data[i]["mcqs_data"] = (
                QuestionsToAskBeforeModel(**questions_data[i])
                .mcqs.values("title", "id")
                .all()
            )
            answer_details = (
                UserAnswerBeforeRelationshipModel.objects.filter(
                    user_id=user_id, question_id=questions_data[i]["id"]
                )
                .order_by("created_at")
                .last()
            )
            questions_data[i]["selected_value"] = 0
            questions_data[i]["selected_answer_id"] = 0
            questions_data[i]["selected_before_match_value"] = 0
            questions_data[i]["selected_before_match_answer_id"] = 0
            if first_message_time_after_match is not None:
                date_time = first_message_time_after_match.created_at
                print(f"date_time {date_time}")
                before_connection_answer_details = (
                    UserAnswerBeforeRelationshipModel.objects.filter(
                        user_id=user_id,
                        question_id=questions_data[i]["id"],
                        created_at__lte=date_time,
                    ).last()
                )
                print(
                    f"before_connection_answer_details {before_connection_answer_details}"
                )
                print(f"questions_data[i]['id'] {questions_data[i]['id']}")
                if before_connection_answer_details is not None:
                    for j in range(0, len(questions_data[i]["mcqs_data"])):
                        if (
                            questions_data[i]["mcqs_data"][j]["id"]
                            == before_connection_answer_details.answer_id
                        ):
                            questions_data[i]["selected_before_match_value"] = j + 1
                    questions_data[i][
                        "selected_before_match_answer_id"
                    ] = before_connection_answer_details.answer_id
            if answer_details is not None:
                for j in range(0, len(questions_data[i]["mcqs_data"])):
                    if (
                        questions_data[i]["mcqs_data"][j]["id"]
                        == answer_details.answer_id
                    ):
                        questions_data[i]["selected_value"] = j + 1
                questions_data[i]["selected_answer_id"] = answer_details.answer_id
            if (
                questions_data[i]["selected_before_match_value"]
                == questions_data[i]["selected_value"]
            ):
                questions_data[i]["selected_before_match_value"] = 0
            if (
                questions_data[i]["selected_before_match_answer_id"]
                == questions_data[i]["selected_answer_id"]
            ):
                questions_data[i]["selected_before_match_answer_id"] = 0
        for j in range(0, len(questions_data)):
            questions_data[j].pop("created_at")
            questions_data[j].pop("updated_at")
        return Response(
            ResponseData.success(questions_data, "Questions fetched successfully"),
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
def get_my_maches(request):
    """Function to get my matches for sending dating request"""
    try:
        data = request.data
        user_id = data["user_id"]
        user = UserModel.objects.filter(id=user_id).first()
        if not user:
            return Response(
                ResponseData.error("User id is invalid"),
                status=status.HTTP_201_CREATED,
            )
        gender_to_search = ""
        this_user_gender = (
            UserHealthDetailsModel.objects.filter(user_id=user_id).first().gender
        )
        if this_user_gender == "Male":
            gender_to_search = "Female"
        else:
            gender_to_search = "Male"
        all_user_ids = (
            UserModel.objects.filter(is_active=True)
            .values("id")
            .exclude(id=user_id)
            .all()
        )
        print(f"all_user_ids {all_user_ids}")
        my_questions_answers = (
            UserAnswerBeforeRelationshipModel.objects.values("question_id", "answer_id")
            .filter(user_id=user_id)
            .all()
        )
        total_questions_count = QuestionsToAskBeforeModel.objects.values().count()
        print(f"total_questions_count {total_questions_count}")
        my_matches_user_ids = []
        for i in range(0, len(all_user_ids)):
            is_user_of_opposite_gender = UserHealthDetailsModel.objects.filter(
                user_id=all_user_ids[i]["id"], gender=gender_to_search
            ).first()
            print(f"is_user_of_opposite_gender {is_user_of_opposite_gender}")
            if is_user_of_opposite_gender is None:
                continue
            number_of_matching_answers = 0
            questions_answers = (
                UserAnswerBeforeRelationshipModel.objects.values(
                    "question_id", "answer_id"
                )
                .filter(user_id=all_user_ids[i]["id"])
                .all()
            )
            for j in range(0, len(questions_answers)):
                for k in range(0, len(my_questions_answers)):
                    if (
                        my_questions_answers[k]["question_id"]
                        == questions_answers[j]["question_id"]
                        and my_questions_answers[k]["answer_id"]
                        == questions_answers[j]["answer_id"]
                    ):
                        number_of_matching_answers += 1
            percentage_match = (
                number_of_matching_answers / total_questions_count
            ) * 100
            if percentage_match > 0:
                my_matches_user_ids.append(all_user_ids[i]["id"])
            print(f"percentage_match {percentage_match}")
            print(f"number_of_matching_answers {number_of_matching_answers}")
        if len(my_matches_user_ids) == 0:
            return Response(
                ResponseData.success_without_data("No match found"),
                status=status.HTTP_201_CREATED,
            )
        result = requests.post(
            "http://127.0.0.1:8000/user_app/getAllUsersDetails/",
            json={
                "filterByCategory": "",
                "filterByDesignation": "",
                "sortBy": "",
                "page_no": "1",
                "page_size": "5",
                "user_id": user_id,
                "my_matches_ids": my_matches_user_ids,
            },
        )
        print(f"result.status_code {result.status_code}")
        if result.status_code == 201:
            print(f"dvdvdddfv {result.json()}")
        return Response(
            ResponseData.success(result.json()["data"], "Matches found successfully"),
            status=status.HTTP_201_CREATED,
        )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
