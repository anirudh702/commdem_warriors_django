from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from food.models import FoodModel, TypeOfFoodModel
from food.serializers import AddFoodSerializer, TypeOfFoodSerializer
from response import Response as ResponseData
from rest_framework import status
from django.core.files.storage import FileSystemStorage
from django.db.models import Q

@api_view(["POST"])
def addFoodType(request):
    """Function to add new food type"""
    try:
        data = request.data
        serializer = TypeOfFoodSerializer(data=data)
        if serializer.is_valid():
            type_of_food_name = serializer.data["type_of_food_name"]
            type_of_food_name_exists = TypeOfFoodModel.objects.filter(type_of_food_name=type_of_food_name).first()
            if type_of_food_name_exists:
                return Response(
                    ResponseData.error(
                        "This food type already exists"),
                    status=status.HTTP_201_CREATED,
                )
            new_data = TypeOfFoodModel.objects.create(
                type_of_food_name=type_of_food_name
            )
            new_data.save()
            return Response(
                ResponseData.success_without_data(
                    "Food type added successfully"),
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
def addFoodItem(request):
    """Function to add new food item"""
    try:
        data = request.data
        serializer = AddFoodSerializer(data=data)
        if serializer.is_valid():
            food_name = serializer.data["food_name"]
            food_image = request.FILES['food_image'] if'food_image' in request.FILES else ''
            type_of_food = serializer.data["type_of_food"]
            is_for_weight_loss = serializer.data['is_for_weight_loss']
            is_veg = serializer.data["is_veg"]
            youtube_url = serializer.data["youtube_url"]
            type_of_food_name_exists = TypeOfFoodModel.objects.filter(id=type_of_food).first()
            if not type_of_food_name_exists:
                return Response(
                    ResponseData.error(
                        "Id of food type is invalid"),
                    status=status.HTTP_201_CREATED,
                )
            food_name_exists = FoodModel.objects.filter(Q(food_name__icontains=food_name)).first()
            if food_name_exists:
                return Response(
                    ResponseData.error(
                        "This food dish already exists in our database"),
                    status=status.HTTP_201_CREATED,
                )
            if food_image!="":
                 fs = FileSystemStorage(location='static/')
                 fs.save(food_image.name, food_image)
            new_data = FoodModel.objects.create(
                food_name=food_name,
                food_image= "" if food_image == "" else f"static/{food_image}",
                type_of_food=TypeOfFoodModel(id=type_of_food),
                is_veg=is_veg,
                youtube_url=youtube_url,
                is_for_weight_loss=is_for_weight_loss
            )
            new_data.save()
            return Response(
                ResponseData.success_without_data(
                    "Food dish added successfully"),
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
def getAllFoodDishes(request):
    """Function to get all food dishes"""
    try:
        data = request.data
        food_dishes_data = FoodModel.objects.values().filter().all()
        for i in range(0,len(food_dishes_data)):
            food_dishes_data[i]['food_dish_type'] = TypeOfFoodModel.objects.values().filter(id=food_dishes_data[i]['type_of_food_id']).get()
            food_dishes_data[i]['food_dish_type'].pop('created_at')
            food_dishes_data[i]['food_dish_type'].pop('updated_at')
            food_dishes_data[i].pop('created_at')
            food_dishes_data[i].pop('updated_at')
            food_dishes_data[i].pop('type_of_food_id')
        if(len(food_dishes_data) == 0):
                return Response(
            ResponseData.success(
                    [], "No food dish found"),
                status=status.HTTP_201_CREATED)
        return Response(
            ResponseData.success(
                    food_dishes_data, "Food dishes details fetched successfully"),
                status=status.HTTP_201_CREATED)
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
