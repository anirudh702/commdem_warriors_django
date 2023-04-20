
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from response import Response as ResponseData
from rest_framework import status
from reviews.models import ReviewModel
from reviews.serializers import AddReviewSerializer, GetReviewSerializer
from user.models import UserPaymentDetailsModel

# Create your views here.

@api_view(["POST"])
def add_review(request):
    """Function to add new review details"""
    try:
        data = request.data
        serializer = AddReviewSerializer(data=data)
        if serializer.is_valid():
            title = serializer.data["title"]

            data_exists = ReviewModel.objects.filter(
                title = title,

                ).first()
            if data_exists:
                   return Response(
                       ResponseData.error("Review with these details already exists"),
                       status=status.HTTP_200_OK,
                   )
            new_review = ReviewModel.objects.create(
                title = title,
            )
            new_review.save()
            return Response(
                ResponseData.success_without_data(
                    "Review added successfully"),
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
def get_review_by_id(request):
    """Function to get a review based on id"""
    try:
        data = request.data
        serializer = GetReviewSerializer(data=data)
        if serializer.is_valid():
            review_id = serializer.data["id"]
            is_id_valid = ReviewModel.objects.filter(id=review_id).first()
            if not is_id_valid:
                   return Response(
                       ResponseData.error("Review id is invalid"),
                       status=status.HTTP_200_OK,
                   )
            review_data = ReviewModel.objects.values().filter(id = review_id).all()
            for i in range(0,len(review_data)):
                review_data[i].pop('created_at')
                review_data[i].pop('updated_at')
            return Response(
                ResponseData.success(
                    review_data, "Review details fetched successfully"),
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
def get_all_review(request):
    """Function to get all review"""
    try:
        data = request.data
        serializer = GetReviewSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data['user_id']
            review_details = list(
            ReviewModel.objects.values().filter())
            can_user_submit_review = False
            current_date = datetime.now()
            get_user_latest_payment_date = UserPaymentDetailsModel.objects.filter(
            user_id = user_id,is_active=True).last().date_of_payment 
            difference_between_both_dates = current_date - get_user_latest_payment_date.replace(tzinfo=None)
            if (difference_between_both_dates.days % 15 == 0):
                can_user_submit_review = True
            for i in range(0,len(review_details)):
                review_details[i].pop('created_at')
                review_details[i].pop('updated_at')
            return Response(
                ResponseData.success_for_get_reviews(
                    review_details, "Review details fetched successfully",can_user_submit_review),
                status=status.HTTP_201_CREATED,)
        return Response(
                    ResponseData.error(serializer.errors),
                    status=status.HTTP_400_BAD_REQUEST,
                )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["POST"])
def delete_review_by_id(request):
    """Function to delete a review based on id"""
    try:
        data = request.data
        serializer = GetReviewSerializer(data=data)
        if serializer.is_valid():
            review_id = serializer.data["id"]
            is_id_valid = ReviewModel.objects.filter(id=review_id).first()
            if not is_id_valid:
                   return Response(
                       ResponseData.error("review id is invalid"),
                       status=status.HTTP_200_OK,
                   )
            review_data = ReviewModel.objects.values().filter(id = review_id).delete()
            return Response(
                ResponseData.success_without_data(
                    "Review of this id deleted successfully"),
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
def delete_all_review(request):
    """Function to delete all review"""
    try:
        data = request.data
        serializer = GetReviewSerializer(data=data)
        if serializer.is_valid():
            review_data = ReviewModel.objects.values().filter().delete()
            return Response(
                ResponseData.success_without_data(
                    "All review deleted successfully"),
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
def update_review(request):
    """Function to update review details"""
    try:
        data = request.data
        serializer = AddReviewSerializer(data=data)
        if serializer.is_valid():
            review_id = serializer.data['id']
            title = serializer.data["title"]

            review_data = ReviewModel.objects.filter(
                id=review_id
            ).first()
            if not review_data:
                return Response(
                    ResponseData.error("Review id is invalid."),
                    status=status.HTTP_200_OK,
                )
            review_data.title=title
            review_data.save()
            updated_data = list(
                ReviewModel.objects.values().filter(
                    id=review_id)
            )
            return Response(
                ResponseData.success(
                    updated_data[0]['id'], "Review details updated successfully"),
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

                  