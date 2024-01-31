from django.core.files.storage import FileSystemStorage
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from advertisement.models import (
    AdvertisementClicksModel,
    AdvertisementModel,
    AdvertisementViewsModel,
)
from advertisement.serializers import (
    AddAdvertisementClickSerializer,
    AddAdvertisementSerializer,
    AddAdvertisementViewSerializer,
    DeleteAdvertisementSerializer,
    GetAdvertisementsSerializer,
    UpdateAdvertisementSerializer,
)
from commdem_warriors_backend.authenticators import ApiKeyAuthentication
from logs.models import LogsOfUserTapOnAdvertisementModel
from response import Response as ResponseData


@api_view(["POST"])
@authentication_classes(
    [
        ApiKeyAuthentication,
    ]
)
def add_new_advertisement(request):
    """Function to add new advertisement"""
    try:
        data = request.data
        serializer = AddAdvertisementSerializer(data=data)
        if serializer.is_valid():
            person_name = serializer.data["person_name"]
            mobile_number = serializer.data["mobile_number"]
            title = serializer.data["title"]
            description = serializer.data["description"]
            image_url = serializer.data["image_url"]
            video_url = serializer.data["video_url"]
            logo = request.FILES["logo"] if "logo" in request.FILES else ""
            advertisement_exists = AdvertisementModel.objects.filter(
                title=title, description=description
            ).first()
            if advertisement_exists:
                return Response(
                    ResponseData.error(
                        "This advertisement title and description already exists"
                    ),
                    status=status.HTTP_201_CREATED,
                )
            if logo != "":
                fs = FileSystemStorage(location="static/")
                fs.save(logo.name, logo)
            new_advertisement = AdvertisementModel.objects.create(
                title=title,
                person_name=person_name,
                description=description,
                mobile_number=mobile_number,
                image_url=image_url,
                video_url=video_url,
                logo="" if logo == "" else f"static/{logo}",
            )
            new_advertisement.save()
            return Response(
                ResponseData.success_without_data(
                    "Advertisement details added successfully"
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
def add_advertisement_logs(request):
    """Function to add advertisement logs"""
    try:
        data = request.data
        user_id = data["user_id"]
        advertisement_id = data["advertisement_id"]
        does_today_data_exists = LogsOfUserTapOnAdvertisementModel.objects.filter(
            user_id=user_id, advertisement_id=advertisement_id
        ).last()
        print(f"does_today_data_exists {does_today_data_exists}")
        if does_today_data_exists is None:
            new_data = LogsOfUserTapOnAdvertisementModel.objects.create(
                user_id=user_id, advertisement_id=advertisement_id, number_of_times=1
            )
            new_data.save()
        else:
            does_today_data_exists.number_of_times = (
                does_today_data_exists.number_of_times + 1
            )
            does_today_data_exists.save()
        return Response(
            ResponseData.success_without_data("Advertisement logs added successfully"),
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
def add_new_advertisement_click(request):
    """Function to add new advertisement click"""
    try:
        data = request.data
        serializer = AddAdvertisementClickSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user"]
            advertisement_id = serializer.data["advertisement"]
            click_date = serializer.data["click_date"]
            new_advertisement_click = AdvertisementClicksModel.objects.create(
                advertisement_id=advertisement_id,
                user_id=user_id,
                click_date=click_date,
            )
            new_advertisement_click.save()
            return Response(
                ResponseData.success_without_data(
                    "Advertisement click details added successfully"
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
def add_new_advertisement_view(request):
    """Function to add new advertisement click"""
    try:
        data = request.data
        serializer = AddAdvertisementViewSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user"]
            advertisement_id = serializer.data["advertisement"]
            view_date = serializer.data["view_date"]
            new_advertisement_view = AdvertisementViewsModel.objects.create(
                advertisement_id=advertisement_id, user_id=user_id, view_date=view_date
            )
            new_advertisement_view.save()
            return Response(
                ResponseData.success_without_data(
                    "Advertisement view details added successfully"
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
def get_all_advertisements(request):
    """Function to get all advertisements"""
    try:
        data = request.data
        serializer = GetAdvertisementsSerializer(data=data)
        if serializer.is_valid():
            advertisement_data = AdvertisementModel.objects.values().filter().all()
            for i in range(0, advertisement_data.count()):
                advertisement_data[i].pop("created_at")
                advertisement_data[i].pop("updated_at")
            return Response(
                ResponseData.success(
                    advertisement_data, "All Advertisements fetched successfully"
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
def delete_advertisement(request):
    """Function to delete an advertisement"""
    try:
        data = request.data
        serializer = DeleteAdvertisementSerializer(data=data)
        if serializer.is_valid():
            id = serializer.data["id"]
            is_advertisement_id_valid = AdvertisementModel.objects.filter(
                id=id, is_active=True
            ).first()
            if not is_advertisement_id_valid:
                return Response(
                    ResponseData.error("This advertisement id does not exists"),
                    status=status.HTTP_200_OK,
                )
            is_advertisement_id_valid.is_active = False
            is_advertisement_id_valid.save()
            return Response(
                ResponseData.success_without_data(
                    "Advertisement details deleted successfully"
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
def update_advertisement(request):
    """Function to update advertisement details"""
    try:
        data = request.data
        print(f"data {data}")
        is_advertisement_id_valid = AdvertisementModel.objects.filter(
            id=request.data["id"], is_active=True
        ).first()
        if not is_advertisement_id_valid:
            return Response(
                ResponseData.error("This advertisement id does not exists"),
                status=status.HTTP_200_OK,
            )
        serializer = UpdateAdvertisementSerializer(data=data)
        if serializer.is_valid():
            title = serializer.data["title"]
            description = serializer.data["description"]
            image_url = (
                request.FILES["image_url"] if "image_url" in request.FILES else ""
            )
            video_url = (
                request.FILES["video_url"] if "video_url" in request.FILES else ""
            )
            ad_type = serializer.data["ad_type"]
            start_date = serializer.data["start_date"]
            end_date = serializer.data["end_date"]
            is_advertisement_id_valid.title = title
            is_advertisement_id_valid.description = description
            is_advertisement_id_valid.image_url = image_url
            is_advertisement_id_valid.video_url = video_url
            is_advertisement_id_valid.ad_type = ad_type
            is_advertisement_id_valid.start_date = start_date
            is_advertisement_id_valid.end_date = end_date
            is_advertisement_id_valid.save()
            return Response(
                ResponseData.success_without_data("Advertisement updated successfully"),
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
