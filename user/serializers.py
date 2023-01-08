"""Serializer for user module"""

from dataclasses import fields
from rest_framework import serializers
from user.models import UserModel, UserPaymentDetailsModel, UserPrivacyModel, UserSubscriptionDetailsModel
from django.contrib.auth import password_validation


class UserSignUpSerializer(serializers.ModelSerializer):
    """Serializer for User sign up details"""
    id = serializers.IntegerField(default=None)
    income_range = serializers.IntegerField(default=None)
    virtual_assistant_language_id = serializers.IntegerField(default=None)
    referral_code = serializers.IntegerField(default=None)
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
        exclude = ["created_at","updated_at","joining_date"]

    # def validate_password(self, value):
    #     """Function for password validation"""
    #     password_validation.validate_password(value, self.instance)
    #     return value

class GetUserProfileSerializer(serializers.ModelSerializer):
    """Serializer for User sign up details"""
    id = serializers.IntegerField()
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = UserModel
        fields = ["id"]

class UserSignInSerializer(serializers.ModelSerializer):
    """Serializer for User sign in details"""
    player_id = serializers.CharField(default=None)
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = UserModel
        fields = ["mobile_number","player_id"]

class AddNewPaymentSerializer(serializers.ModelSerializer):
    """Serializer for adding new payment details"""
    user_id=serializers.IntegerField(default=None)
    subscription_id=serializers.IntegerField(default=None)
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = UserPaymentDetailsModel
        exclude = ["created_at","updated_at"]

class UpdateUserPrivacySerializer(serializers.ModelSerializer):
    """Serializer for updating user privacy settings"""
    user=serializers.IntegerField(default=None)
    is_age_hidden=serializers.BooleanField(default=None)
    is_city_hidden=serializers.BooleanField(default=None)
    is_mobile_number_hidden=serializers.BooleanField(default=None)
    is_designation_title_hidden=serializers.BooleanField(default=None)
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = UserPrivacyModel
        fields = ["user","is_age_hidden","is_city_hidden","is_mobile_number_hidden","is_designation_title_hidden"]

class AddUserSubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for adding new subscription details of a user"""
    user_id = serializers.IntegerField(default=None)
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = UserSubscriptionDetailsModel
        exclude = ["created_at","updated_at"]

class GetUserSubscriptionSerializer(serializers.ModelSerializer):
    """Serializer to get subscription details of a user"""
    id = serializers.IntegerField(default=None)
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = UserSubscriptionDetailsModel
        exclude = ["id","user"]

class UserSubscribedOrNotSerializer(serializers.ModelSerializer):
    """Serializer for checking if user is subscribed or not"""
    id = serializers.IntegerField()
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = UserModel
        fields = ['id']

class GetAllUsersDetailsSerializer(serializers.ModelSerializer):
    """Serializer for getting details of all users"""
    id = serializers.IntegerField(default=None)
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = UserModel
        fields = ['id']
