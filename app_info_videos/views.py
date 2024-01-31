from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from app_info_videos.models import AppInfoVideosModel
from app_info_videos.serializers import (
    AddAppInfoVideosSerializer,
    GetAppInfoVideosSerializer,
)
from commdem_warriors_backend.authenticators import ApiKeyAuthentication
from response import Response as ResponseData

# Create your views here.


@api_view(["POST"])
@authentication_classes(
    [
        ApiKeyAuthentication,
    ]
)
def add_app_info_videos(request):
    """Function to add new app_info_videos details"""
    try:
        data = request.data
        serializer = AddAppInfoVideosSerializer(data=data)
        if serializer.is_valid():
            title = serializer.data["title"]
            video_url = serializer.data["video_url"]

            data_exists = AppInfoVideosModel.objects.filter(
                title=title, video_url=video_url
            ).first()
            if data_exists:
                return Response(
                    ResponseData.error(
                        "AppInfoVideos with these details already exists"
                    ),
                    status=status.HTTP_200_OK,
                )
            new_app_info_videos = AppInfoVideosModel.objects.create(
                title=title, video_url=video_url
            )
            new_app_info_videos.save()
            return Response(
                ResponseData.success_without_data("AppInfoVideos added successfully"),
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
def get_all_app_info_videos(request):
    """Function to get all app_info_videos"""
    try:
        data = request.data
        serializer = GetAppInfoVideosSerializer(data=data)
        if serializer.is_valid():
            app_info_videos_details = list(AppInfoVideosModel.objects.values().filter())
            for i in range(0, len(app_info_videos_details)):
                app_info_videos_details[i].pop("created_at")
                app_info_videos_details[i].pop("updated_at")
            return Response(
                ResponseData.success(
                    app_info_videos_details,
                    "AppInfoVideos details fetched successfully",
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
def delete_app_info_videos_by_id(request):
    """Function to delete a app_info_videos based on id"""
    try:
        data = request.data
        serializer = GetAppInfoVideosSerializer(data=data)
        if serializer.is_valid():
            app_info_videos_id = serializer.data["id"]
            is_id_valid = AppInfoVideosModel.objects.filter(
                id=app_info_videos_id
            ).first()
            if not is_id_valid:
                return Response(
                    ResponseData.error("app_info_videos id is invalid"),
                    status=status.HTTP_200_OK,
                )
            (AppInfoVideosModel.objects.values().filter(id=app_info_videos_id).delete())
            return Response(
                ResponseData.success_without_data(
                    "AppInfoVideos of this id deleted successfully"
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
def delete_all_app_info_videos(request):
    """Function to delete all app_info_videos"""
    try:
        data = request.data
        serializer = GetAppInfoVideosSerializer(data=data)
        if serializer.is_valid():
            AppInfoVideosModel.objects.values().filter().delete()
            return Response(
                ResponseData.success_without_data(
                    "All app_info_videos deleted successfully"
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
def update_app_info_videos(request):
    """Function to update app_info_videos details"""
    try:
        data = request.data
        serializer = AddAppInfoVideosSerializer(data=data)
        if serializer.is_valid():
            app_info_videos_id = serializer.data["id"]
            title = serializer.data["title"]

            app_info_videos_data = AppInfoVideosModel.objects.filter(
                id=app_info_videos_id
            ).first()
            if not app_info_videos_data:
                return Response(
                    ResponseData.error("AppInfoVideos id is invalid."),
                    status=status.HTTP_200_OK,
                )
            if "image" in request.FILES:
                fs = FileSystemStorage(location="static/")
                fs.save(request.FILES["image"].name, request.FILES["image"])
            app_info_videos_data.title = title

            # if 'image' in request.FILES:
            #   userdata.profile_pic = f"static/{request.FILES['image']}"
            app_info_videos_data.save()
            updated_data = list(
                AppInfoVideosModel.objects.values().filter(id=app_info_videos_id)
            )
            return Response(
                ResponseData.success(
                    updated_data[0]["id"], "AppInfoVideos details updated successfully"
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
