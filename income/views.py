from rest_framework.decorators import api_view
from rest_framework.response import Response
from income.models import IncomeModel
from response import Response as ResponseData
from rest_framework import status
# Create your views here.

@api_view(["POST"])
def add_new_income_range(request):
    """Function to add new income range details"""
    try:
        data = request.data
        final_data = []
        for i in range(0,len(data)):
            data_exist_or_not = IncomeModel.objects.filter(income_range=data[i]).first()
            if data_exist_or_not:
                return Response(
                    ResponseData.error("Data already exists"),
                    status=status.HTTP_200_OK,
                )
            final_data.append(IncomeModel(
                income_range=data[i]
                ))
        IncomeModel.objects.bulk_create(final_data)
        return Response(
            ResponseData.success(
                [], "Income range details added successfully"),
            status=status.HTTP_201_CREATED,
        )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["POST"])
def get_all_income_range(request):
    """Function to get all income range details"""
    try:
        income_range_data = IncomeModel.objects.values().filter().all()
        for i in range(0,income_range_data.count()):
            income_range_data[i].pop('created_at')
            income_range_data[i].pop('updated_at')
        return Response(
            ResponseData.success(
                income_range_data, "Income range details fetched successfully"),
            status=status.HTTP_201_CREATED)
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )