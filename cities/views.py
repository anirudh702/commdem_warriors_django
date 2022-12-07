from rest_framework.decorators import api_view
from cities.models import CitiesModel
from rest_framework.response import Response
from response import Response as ResponseData
from rest_framework import status
# Create your views here.

@api_view(["POST"])
def add_new_city(request):
    """Function to add new city details"""
    try:
        data = request.data
        final_data = []
        for i in range(0,data.count()):
            data_exist_or_not = CitiesModel.objects.filter(name=data[i]['name']).first()
            if data_exist_or_not:
                return Response(
                    ResponseData.error("Data already exists"),
                    status=status.HTTP_200_OK,
                )
            final_data.append(CitiesModel(
                name=data[i]['name'],
                state=data[i]['state'],
                ))
        CitiesModel.objects.bulk_create(final_data)
        return Response(
            ResponseData.success(
                [], "Cities details added successfully"),
            status=status.HTTP_201_CREATED,
        )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["POST"])
def get_all_cities(request):
    """Function to get all cities details"""
    try:
        cities_data = CitiesModel.objects.values().filter().all()
        for i in range(0,cities_data.count()):
            cities_data[i].pop('created_at')
            cities_data[i].pop('updated_at')
        return Response(
            ResponseData.success(
                cities_data, "Cities details fetched successfully"),
            status=status.HTTP_201_CREATED)
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )