import subprocess
from datetime import datetime

from django.core.files.storage import FileSystemStorage
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from commdem_warriors_backend.authenticators import ApiKeyAuthentication
from commitment.models import CommitmentModel, CommitmentNameModel
from response import Response as ResponseData
from user.models import UserModel
from warriors_workout_videos.models import WarriorsWorkoutVideosModel
from warriors_workout_videos.serializers import (
    AddWarriorsWorkoutVideoSerializer,
    GetWarriorsWorkoutVideoSerializer,
)


def returnCapturedImage(workout_file, user_id, commitment_id, hour, minute, second):
    # Replace these variables with your input and output file paths
    input_video = f"static{workout_file}"
    print(f"input_video {input_video}")
    output_image = (
        f"static/{user_id}_{commitment_id}_{str(hour)}_{str(minute)}_{str(second)}.jpg"
    )

    # Specify the time to capture (5 seconds)
    time_to_capture = "00:00:03"

    # FFmpeg command to capture the frame
    ffmpeg_command = [
        "ffmpeg",
        "-i",
        input_video,
        "-ss",
        time_to_capture,
        "-vframes",
        "1",
        output_image,
    ]
    print(f"dfvfvfvfdv {ffmpeg_command}")
    # Run the FFmpeg command
    try:
        subprocess.run(ffmpeg_command, check=True)
        print(f"Frame from {time_to_capture} saved as {output_image}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    return output_image


# Create your views here.
@api_view(["POST"])
@authentication_classes(
    [
        ApiKeyAuthentication,
    ]
)
def add_warrior_workout(request):
    """Function to upload video/image of a workout done by warrior"""
    try:
        data = request.data
        print(f"data {data}")
        serializer = AddWarriorsWorkoutVideoSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            commitment_id = serializer.data["commitment_id"]
            description = serializer.data["description"]
            workout_file = request.FILES["workout_file"]
            user = UserModel.objects.filter(id=user_id, is_active=True).first()
            if not user:
                return Response(
                    ResponseData.error("User id is invalid"),
                    status=status.HTTP_200_OK,
                )
            commitment = CommitmentModel.objects.filter(id=commitment_id).first()
            if not commitment:
                return Response(
                    ResponseData.error("Commitment id is invalid"),
                    status=status.HTTP_200_OK,
                )
            hour = datetime.now().hour
            minute = datetime.now().minute
            second = datetime.now().second
            saved_file_name = (
                f"{user.id}_{commitment_id}_{str(hour)}_{str(minute)}_{str(second)}.mp4"
            )
            if workout_file != "" or workout_file is not None:
                fs = FileSystemStorage(location="static/")
                finalWorkoutFile = fs.save(saved_file_name, workout_file)
                workout_thumbnail = returnCapturedImage(
                    fs.url(finalWorkoutFile),
                    user.id,
                    commitment_id,
                    hour,
                    minute,
                    second,
                )
                print(f"workout_thumbnail {workout_thumbnail}")
            new_data = WarriorsWorkoutVideosModel.objects.create(
                user_id=user_id,
                commitment_id=commitment_id,
                description=description,
                workout_file=f"static/{saved_file_name}",
                workout_thumbnail_file=workout_thumbnail,
            )
            new_data.save()
            return Response(
                ResponseData.success_without_data("Workout data uploaded successfully"),
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
def get_all_warriors_workout(request):
    """Function to get workout files of all warriors""" 
    try:
        data = request.data
        print(f"data {data}")
        serializer = GetWarriorsWorkoutVideoSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            user = UserModel.objects.filter(id=user_id, is_active=True).first()
            if not user:
                return Response(
                    ResponseData.error("User id is invalid"),
                    status=status.HTTP_200_OK,
                )
            workout_data = WarriorsWorkoutVideosModel.objects.values().filter().all()
            for i in range(0, len(workout_data)):
                workout_data[i].pop("created_at")
                workout_data[i].pop("updated_at")
                workout_data[i].pop("is_private_for_all")
                workout_data[i].pop("private_for_this_gender")
                commitment_details = CommitmentModel.objects.filter(
                    id=workout_data[i]["commitment_id"]
                ).last()
                print(f"commitment_details {commitment_details}")
                if commitment_details is not None:
                    workout_data[i]["commitment_name"] = (
                        CommitmentNameModel.objects.filter(
                            id=commitment_details.commitment_name_id
                        )
                        .last()
                        .mainTitle
                    )
            return Response(
                ResponseData.success(
                    workout_data, "Warriors workout fetched successfully"
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
