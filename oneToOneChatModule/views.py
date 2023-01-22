from datetime import timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from oneToOneChatModule.models import OneToOneChatModel, OneToOneFilesSharedOnChatModel
from oneToOneChatModule.serializers import AddNewChatSerializer, GetUsersWithChatSerializer
from response import Response as ResponseData
from rest_framework import status
from django.core.files.storage import FileSystemStorage
from user.models import UserModel
from django.db.models import Q

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
            # return web.Response(text=json.dumps(ResponseData.success_without_data(
            #         "New chat added successfully"),), status=200)
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
def display_chat_users_details(request):
    """Function to get list of users with whom particular user did chat"""
    try:
        data = request.data
        serializer = GetUsersWithChatSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            users_data = UserModel.objects.all().exclude(id=user_id)
            if len(users_data) == 0:
                return Response(
                ResponseData.success_without_data(
                    "No other user found in the group"),
                status=status.HTTP_201_CREATED,
            )
            final_data = []
            for i in range(0,len(users_data)):
                print("sdcdscsd")
                mapData = {}
                chat_data = OneToOneChatModel.objects.filter((Q(from_user_id=user_id) & Q(to_user_id=users_data[i].id)) | (Q(from_user_id=users_data[i].id) & Q(to_user_id=user_id)) ).order_by('-created_at').first()
                print(f"chat_data {chat_data}")
                if chat_data is not None:
                    mapData['user_full_name'] = users_data[i].full_name
                    mapData['user_id'] = users_data[i].id
                    mapData['user_profile_pic'] = str(users_data[i].profile_pic)
                    mapData['latest_message'] = chat_data.chat_message
                    mapData['is_message_seen'] = chat_data.is_message_seen
                    mapData['created_at'] = chat_data.created_at + timedelta(hours=5, minutes=30)
                    final_data.append(mapData)
            final_data = sorted(final_data, key=lambda d: d['created_at'],reverse=True)
            if(len(final_data) == 0):  
                return Response(
                ResponseData.success_without_data(
                    "No details found"),
                status=status.HTTP_201_CREATED,
            )            
            return Response(
                ResponseData.success(final_data,
                    "Details fetched successfully"),
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

