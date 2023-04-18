
from rest_framework.decorators import api_view
from rest_framework.response import Response
from response import Response as ResponseData
from rest_framework import status
from challenges_result.models import ChallengesResultModel
from challenges_result.serializers import AddChallengesResultSerializer, GetChallengesResultSerializer
from user.models import UserModel

# Create your views here.

@api_view(["POST"])
def add_challenges_result(request):
    """Function to add new challenges_result details"""
    try:
        data = request.data
        serializer = AddChallengesResultSerializer(data=data)
        if serializer.is_valid():

            data_exists = ChallengesResultModel.objects.filter(competition_id = serializer['competition_id']).first()
            if data_exists:
                   return Response(
                       ResponseData.error("ChallengesResult with these details already exists"),
                       status=status.HTTP_200_OK,
                   )
            new_challenges_result = ChallengesResultModel.objects.create(
               user_id = serializer['user_id'],
               competition_id = serializer['competition_id'],
               rank = serializer['rank'],
               description = serializer['description'],
               prize_money = serializer['prize_money']
            )
            new_challenges_result.save()
            return Response(
                ResponseData.success_without_data(
                    "Challenges Result added successfully"),
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
def get_challenges_result_by_id(request):
    """Function to get a challenges_result based on id"""
    try:
        data = request.data
        serializer = GetChallengesResultSerializer(data=data)
        if serializer.is_valid():
            competition_id = serializer.data["competition_id"]
            is_id_valid = ChallengesResultModel.objects.filter(competition_id=competition_id).first()
            if not is_id_valid:
                   return Response(
                       ResponseData.error("ChallengesResult id is invalid"),
                       status=status.HTTP_200_OK,
                   )
            challenges_result_data = ChallengesResultModel.objects.values().filter(competition_id = competition_id).order_by('rank').all()
            for i in range(0,len(challenges_result_data)):
                challenges_result_data[i]['fullname'] = UserModel.objects.filter(id=challenges_result_data[i]['user_id'],is_active=True).first().full_name
                challenges_result_data[i].pop('created_at')
                challenges_result_data[i].pop('updated_at')
            return Response(
                ResponseData.success(
                    challenges_result_data, "ChallengesResult details fetched successfully"),
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
def get_all_challenges_result(request):
    """Function to get all challenges_result"""
    try:
        data = request.data
        serializer = GetChallengesResultSerializer(data=data)
        if serializer.is_valid():
                challenges_result_details = list(
                ChallengesResultModel.objects.values().filter())
                for i in range(0,len(challenges_result_details)):
                    challenges_result_details[i].pop('created_at')
                    challenges_result_details[i].pop('updated_at')
                return Response(
                    ResponseData.success(
                        challenges_result_details, "ChallengesResult details fetched successfully"),
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
def delete_challenges_result_by_id(request):
    """Function to delete a challenges_result based on id"""
    try:
        data = request.data
        serializer = GetChallengesResultSerializer(data=data)
        if serializer.is_valid():
            challenges_result_id = serializer.data["id"]
            is_id_valid = ChallengesResultModel.objects.filter(id=challenges_result_id).first()
            if not is_id_valid:
                   return Response(
                       ResponseData.error("challenges_result id is invalid"),
                       status=status.HTTP_200_OK,
                   )
            challenges_result_data = ChallengesResultModel.objects.values().filter(id = challenges_result_id).delete()
            return Response(
                ResponseData.success_without_data(
                    "ChallengesResult of this id deleted successfully"),
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
def delete_all_challenges_result(request):
    """Function to delete all challenges_result"""
    try:
        data = request.data
        serializer = GetChallengesResultSerializer(data=data)
        if serializer.is_valid():
            challenges_result_data = ChallengesResultModel.objects.values().filter().delete()
            return Response(
                ResponseData.success_without_data(
                    "All challenges_result deleted successfully"),
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
def update_challenges_result(request):
    """Function to update challenges_result details"""
    try:
        data = request.data
        serializer = AddChallengesResultSerializer(data=data)
        if serializer.is_valid():
            challenges_result_id = serializer.data['id']

            challenges_result_data = ChallengesResultModel.objects.filter(
                id=challenges_result_id
            ).first()
            if not challenges_result_data:
                return Response(
                    ResponseData.error("ChallengesResult id is invalid."),
                    status=status.HTTP_200_OK,
                )
            if 'image' in request.FILES:
                fs = FileSystemStorage(location='static/')
                fs.save(request.FILES['image'].name, request.FILES['image'])

            #if 'image' in request.FILES:
            #   userdata.profile_pic = f"static/{request.FILES['image']}"
            challenges_result_data.save()
            updated_data = list(
                ChallengesResultModel.objects.values().filter(
                    id=challenges_result_id)
            )
            return Response(
                ResponseData.success(
                    updated_data[0]['id'], "ChallengesResult details updated successfully"),
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

                  