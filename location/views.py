from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from commdem_warriors_backend.authenticators import ApiKeyAuthentication
from location.models import (
    CitiesModel,
    CountriesDialCodeModel,
    CountriesModel,
    StatesModel,
)
from response import Response as ResponseData

# Create your views here.


@api_view(["POST"])
@authentication_classes(
    [
        ApiKeyAuthentication,
    ]
)
def addCountryDialCodes(request):
    """Function to add new cities,states,countries"""
    try:
        data = request.data
        for i in range(0, data.count()):
            data_exist_or_not = CountriesDialCodeModel.objects.filter(
                country_code=data[i]["code"]
            ).first()
            if data_exist_or_not is None:
                new_country = CountriesDialCodeModel.objects.create(
                    country_dial_code=data[i]["dial_code"],
                    country_code=data[i]["code"],
                    country_name=data[i]["name"],
                )
                new_country.save()
        return Response(
            ResponseData.success([], "Data added successfully"),
            status=status.HTTP_201_CREATED,
        )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def get_all_countries(request):
    """Function to get all countries details"""
    try:
        # send_to_firebase()
        countries_data = CountriesModel.objects.values().filter().all()
        for i in range(0, len(countries_data)):
            countries_data[i].pop("created_at")
            countries_data[i].pop("updated_at")
        return Response(
            ResponseData.success(
                countries_data, "Countries details fetched successfully"
            ),
            status=status.HTTP_201_CREATED,
        )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def get_all_states_of_country(request):
    """Function to get all states details of a country"""
    try:
        country_id = request.data["id"]
        state_data = StatesModel.objects.values().filter(country_id=country_id).all()
        for i in range(0, len(state_data)):
            state_data[i].pop("created_at")
            state_data[i].pop("updated_at")
        return Response(
            ResponseData.success(state_data, "State details fetched successfully"),
            status=status.HTTP_201_CREATED,
        )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def get_all_cities_of_state(request):
    """Function to get all cities details of a state"""
    try:
        state_id = request.data["id"]
        cities_data = CitiesModel.objects.values().filter(state_id=state_id).all()
        for i in range(0, len(cities_data)):
            cities_data[i].pop("created_at")
            cities_data[i].pop("updated_at")
        return Response(
            ResponseData.success(cities_data, "Cities details fetched successfully"),
            status=status.HTTP_201_CREATED,
        )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
