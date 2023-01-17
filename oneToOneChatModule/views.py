from rest_framework.decorators import api_view
from rest_framework.response import Response
from oneToOneChatModule.models import OneToOneChatModel, OneToOneFilesSharedOnChatModel
from oneToOneChatModule.serializers import AddNewChatSerializer
from response import Response as ResponseData
from rest_framework import status
from django.core.files.storage import FileSystemStorage
from user.models import UserModel

# Create your views here.
@api_view(["POST"])
def add_new_chat_between_two_users(request):
    """Function to add new chat between 2 users"""
    try:
        data = request.data
        serializer = AddNewChatSerializer(data=data)
        if serializer.is_valid():
            from_user_id = serializer.data["from_user_id"]
            to_user_id = serializer.data["to_user_id"]
            chat_message = serializer.data['chat_message'] if'chat_message' in request.data else ''
            files_path = request.FILES['files_path'] if'files_path' in request.FILES else None
            new_data = OneToOneChatModel.objects.create(
                from_user_id=from_user_id,
                to_user_id=to_user_id,
                chat_message = chat_message,
            )
            new_data.save()
            if files_path is not None:
                for i in range(0,len(files_path)):
                    new_file_data = OneToOneFilesSharedOnChatModel.objects.create(
                    path = files_path[i],
                    chat_id=new_data.id
                    )    
                    new_file_data.save()
                    fs = FileSystemStorage(location='static/')
                    fs.save(files_path[i].name, files_path[i])
            return Response(
                ResponseData.success_without_data(
                    "New chat added successfully"),
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
def upload_video_for_group_challenge(request):
    """Function to upload challenge video of a user"""
    try:
        data = request.data
        print(f"data {data}")
        serializer = UploadVideoOfUserGroupChallengeSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            group_challenge_id = serializer.data["group_challenge_id"]
            video_file = request.FILES['video_file']
            user = UserModel.objects.filter(id=user_id,is_active=True).first()
            if not user:
                   return Response(
                       ResponseData.error("User id is invalid"),
                       status=status.HTTP_200_OK,
                   )
            group_challenge = GroupChallengesModel.objects.filter(id=group_challenge_id).first()
            if not group_challenge:
                   return Response(
                       ResponseData.error("Group challenge id is invalid"),
                       status=status.HTTP_200_OK,
                   )
            user_challenge_data = ParticipantsInGroupChallengeModel.objects.filter(user_id=user_id,group_challenge_id=group_challenge_id,hide_from_user=False).get()
            if user_challenge_data is None:
                return Response(
                       ResponseData.error("You are not a participant yet. Please participate first."),
                       status=status.HTTP_200_OK,
                   )
            user_challenge_data.challenge_video = f"static/{video_file}"
            user_challenge_data.has_submitted_video = True
            user_challenge_data.save()
            if video_file!="" or video_file is not None:
                 fs = FileSystemStorage(location='static/')
                 fs.save(video_file.name, video_file)
            return Response(
                ResponseData.success_without_data(
                    "Video uploaded successfully"),
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
def update_user_participation_for_group_challenge(request):
    """Function to update user particiation for group challenge"""
    try:
        data = request.data
        serializer = UpdateUserParticipationStatusInGroupChallengeSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            group_challenge_id = serializer.data["group_challenge_id"]
            want_to_participate = serializer.data['want_to_participate']
            user = UserModel.objects.filter(id=user_id,is_active=True).first()
            if not user:
                   return Response(
                       ResponseData.error("User id is invalid"),
                       status=status.HTTP_200_OK,
                   )
            group_challenge = GroupChallengesModel.objects.filter(id=group_challenge_id).first()
            if not group_challenge:
                   return Response(
                       ResponseData.error("Group challenge id is invalid"),
                       status=status.HTTP_200_OK,
                   )
            user_challenge_data = ParticipantsInGroupChallengeModel.objects.filter(user_id=user_id,group_challenge_id=group_challenge_id).get()
            if user_challenge_data is None:
                return Response(
                       ResponseData.error("You are not a participant yet. Please participate first."),
                       status=status.HTTP_200_OK,
                   )
            if want_to_participate == False:
                user_challenge_data.hide_from_user = True
                user_challenge_data.save()
            else:
                user_challenge_data.hide_from_user = False
                user_challenge_data.save()
            return Response(
                ResponseData.success_without_data(
                    "Status updated successfully"),
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