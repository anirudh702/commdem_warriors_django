"""Serializer for user module"""

from rest_framework import serializers

from user.models import (
    UserAnswerBeforeRelationshipModel,
    UserModel,
    UserPaymentDetailsModel,
    UserPrivacyModel,
    UserReviewModel,
    UserSubscriptionDetailsModel,
)


class UserSignUpSerializer(serializers.ModelSerializer):
    """Serializer for User sign up details"""

    id = serializers.IntegerField(default=None)
    income_range = serializers.IntegerField(default=None)
    virtual_assistant_language_id = serializers.IntegerField(default=None)
    referred_user_phone_number = serializers.CharField(default=None)
    referred_user_full_name = serializers.CharField(default=None)
    player_id = serializers.CharField(default=None)
    user_uid = serializers.CharField(default=None)
    designation_title = serializers.CharField(default=None)
    gender = serializers.CharField(default=None)
    designation = serializers.IntegerField(default=None)
    weight = serializers.FloatField(default=None)
    height = serializers.IntegerField(default=None)
    city_id = serializers.IntegerField(default=None)
    state_id = serializers.IntegerField(default=None)
    country_id = serializers.IntegerField(default=None)
    age = serializers.IntegerField(default=None)
    user_gmail_id = serializers.EmailField(default=None)
    is_medicine_ongoing = serializers.BooleanField(default=None)
    any_health_issues = serializers.BooleanField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = UserModel
        exclude = ["created_at", "updated_at", "joining_date"]

    # def validate_password(self, value):
    #     """Function for password validation"""
    #     password_validation.validate_password(value, self.instance)
    #     return value


class GetUserProfileSerializer(serializers.ModelSerializer):
    """Serializer for User sign up details"""

    id = serializers.IntegerField()
    other_user_id = serializers.IntegerField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = UserModel
        fields = ["id", "other_user_id"]


class UserSignInSerializer(serializers.ModelSerializer):
    """Serializer for User sign in details"""

    player_id = serializers.CharField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = UserModel
        fields = ["mobile_number", "player_id"]


class AddNewPaymentSerializer(serializers.ModelSerializer):
    """Serializer for adding new payment details"""

    user_id = serializers.IntegerField(default=None)
    payment_id = serializers.CharField(default=None)
    date_of_payment = serializers.CharField(default=None)
    challenge_type = serializers.CharField(default=None)
    subscription_id = serializers.IntegerField(default=None)
    group_challenge_id = serializers.IntegerField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = UserPaymentDetailsModel
        fields = [
            "challenge_type",
            "user_id",
            "payment_id",
            "subscription_id",
            "group_challenge_id",
            "date_of_payment",
        ]


class UpdateUserPrivacySerializer(serializers.ModelSerializer):
    """Serializer for updating user privacy settings"""

    user = serializers.IntegerField(default=None)
    other_user = serializers.IntegerField(default=None)
    is_age_hidden = serializers.BooleanField(default=None)
    is_city_hidden = serializers.BooleanField(default=None)
    is_mobile_number_hidden = serializers.BooleanField(default=None)
    is_designation_title_hidden = serializers.BooleanField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = UserPrivacyModel
        fields = [
            "user",
            "other_user",
            "is_age_hidden",
            "is_city_hidden",
            "is_mobile_number_hidden",
            "is_designation_title_hidden",
        ]


class AddUserSubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for adding new subscription details of a user"""

    user_id = serializers.IntegerField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = UserSubscriptionDetailsModel
        exclude = ["created_at", "updated_at"]


class GetUserSubscriptionSerializer(serializers.ModelSerializer):
    """Serializer to get subscription details of a user"""

    id = serializers.IntegerField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = UserSubscriptionDetailsModel
        exclude = ["id", "user"]


class UserSubscribedOrNotSerializer(serializers.ModelSerializer):
    """Serializer for checking if user is subscribed or not"""

    id = serializers.IntegerField()

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = UserModel
        fields = ["id"]


class GetAllUsersDetailsSerializer(serializers.ModelSerializer):
    """Serializer for getting details of all users"""

    id = serializers.IntegerField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = UserModel
        fields = ["id"]


class AddUserReviewSerializer(serializers.ModelSerializer):
    """Serializer for adding review by user"""

    user_id = serializers.IntegerField(default=None)
    data_of_all_reviews = serializers.ListField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = UserReviewModel
        fields = ["user_id", "data_of_all_reviews"]


class AddAnswersOfQuestionsBeforeRelationshipSerializer(serializers.ModelSerializer):
    """Serializer for adding answers of questions user gave before relationship"""

    user_id = serializers.IntegerField(default=None)
    data_of_all_questions = serializers.ListField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = UserAnswerBeforeRelationshipModel
        fields = ["user_id", "data_of_all_questions"]


class UpdateUserReviewSerializer(serializers.ModelSerializer):
    """Serializer for updating user review details"""

    user_id = serializers.IntegerField(default=None)
    review_id = serializers.IntegerField(default=None)
    star_rating = serializers.IntegerField(default=None)
    description = serializers.CharField(default=None)
    review_date = serializers.DateTimeField(default=None)
    user_review_id = serializers.IntegerField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = UserReviewModel
        fields = [
            "user_id",
            "review_id",
            "star_rating",
            "description",
            "review_date",
            "user_review_id",
        ]


class GetReviewsOfAllUsersSerializer(serializers.ModelSerializer):
    """Serializer for getting reviews of all users"""

    page_no = serializers.IntegerField(default=None)
    page_size = serializers.IntegerField(default=None)
    star_rating = serializers.CharField(default=None)
    search = serializers.CharField(default=None)
    start_date = serializers.CharField(default=None)
    end_date = serializers.CharField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""

        model = UserReviewModel
        fields = [
            "page_no",
            "page_size",
            "star_rating",
            "search",
            "start_date",
            "end_date",
        ]
