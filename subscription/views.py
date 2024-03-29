from rest_framework.decorators import api_view
from rest_framework.response import Response
from designation.models import DesignationModel
from response import Response as ResponseData
from rest_framework import status
from subscription.models import SubscriptionModel
from subscription.serializers import AddSubscriptionSerializer, GetSubscriptionSerializer
from user.models import UserPaymentDetailsModel, UserProfessionalDetailsModel, UserSubscriptionDetailsModel

# Create your views here.

@api_view(["POST"])
def add_subscription(request):
    """Function to add new subscription details"""
    try:
        data = request.data
        serializer = AddSubscriptionSerializer(data=data)
        if serializer.is_valid():
            amount = serializer.data["amount"]
            duration = serializer.data['duration']
            is_free_trial = serializer.data['is_free_trial']
            designation_id = serializer.data['designation_id']
            is_id_valid = DesignationModel.objects.using('designation_db').filter(id=designation_id).first()
            if not is_id_valid:
                   return Response(
                       ResponseData.error("This designation id does not exists"),
                       status=status.HTTP_200_OK,
                   )
            data_exists = SubscriptionModel.objects.using('subscription_db').filter(
                amount = amount,duration=duration,designation_id=is_id_valid.id).first()
            if data_exists:
                   return Response(
                       ResponseData.error("Subscription with these details already exists"),
                       status=status.HTTP_200_OK,
                   )
            new_subscription = SubscriptionModel.objects.using('subscription_db').create(
                amount = amount,
                duration = duration,
                is_free_trial = is_free_trial,
                designation_id=is_id_valid.id
            )
            new_subscription.save()
            return Response(
                ResponseData.success(
                    [], "Subscription added successfully"),
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
def get_subscription_by_id(request):
    """Function to get a subscription based on id"""
    try:
        data = request.data
        serializer = GetSubscriptionSerializer(data=data)
        if serializer.is_valid():
            subscription_id = serializer.data["id"]
            is_id_valid = SubscriptionModel.objects.using('subscription_db').filter(id=subscription_id).first()
            if not is_id_valid:
                   return Response(
                       ResponseData.error("Subscription id is invalid"),
                       status=status.HTTP_200_OK,
                   )
            subscription_data = SubscriptionModel.objects.using('subscription_db').values().filter(id = subscription_id).all()
            for i in range(0,subscription_data.count()):
                subscription_data[i].pop('created_at')
                subscription_data[i].pop('updated_at')
            return Response(
                ResponseData.success(
                    subscription_data, "Subscription details fetched successfully"),
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
def get_all_subscriptions(request):
    """Function to get all subscriptions"""
    try:
        data = request.data
        serializer = GetSubscriptionSerializer(data=data)
        if serializer.is_valid():
                user_id = serializer.data['user_id']
                is_user_id_valid = UserProfessionalDetailsModel.objects.using('user_db').filter(user_id=user_id).first()
                if not is_user_id_valid:
                   return Response(
                       ResponseData.error("This user does not exists"),
                       status=status.HTTP_200_OK,
                   )
                subscription_details = list(
                SubscriptionModel.objects.using('subscription_db').values().filter(
                    designation_id=is_user_id_valid.designation_id
                ))
                for i in range(0,len(subscription_details)):
                    subscription_details[i].pop('created_at')
                    subscription_details[i].pop('updated_at')
                return Response(
                    ResponseData.success(
                        subscription_details, "Subscription details fetched successfully"),
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
def get_past_subscriptions_of_user(request):
    """Function to get all past subscriptions of user"""
    try:
        data = request.data
        serializer = GetSubscriptionSerializer(data=data)
        if serializer.is_valid():
                user_id = serializer.data['user_id']
                payment_details = list(UserPaymentDetailsModel.objects.using('user_db').values().filter(user_id=user_id,is_active=True))
                if len(payment_details) == 0:
                   return Response(
                       ResponseData.error("No subscriptions found"),
                       status=status.HTTP_200_OK,
                   )
                all_payment_details = []
                print("called")
                for i in range(0,len(payment_details)):
                    print(payment_details[i]['subscription_id'])
                    subscription_details = list(SubscriptionModel.objects.using('subscription_db').values().filter(
                         id=payment_details[i]['subscription_id']
                     ))
                    if len(subscription_details) == 0:
                        return Response(
                       ResponseData.error("Subscription id is invalid"),
                       status=status.HTTP_200_OK,
                   )
                    subscription_details[0].pop('updated_at')
                    subscription_details[0].pop('created_at')
                    payment_details[i].pop('updated_at')
                    payment_details[i].pop('created_at')
                    payment_details[i]['subscription_details'] = subscription_details[0]
                    all_payment_details.append(payment_details[i])
                return Response(
                    ResponseData.success(
                        all_payment_details, "User past Subscription details fetched successfully"),
                    status=status.HTTP_201_CREATED)
        return Response(
                    ResponseData.error(serializer.errors),
                    status=status.HTTP_400_BAD_REQUEST,
                )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )