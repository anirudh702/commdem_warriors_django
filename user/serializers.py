"""Serializer for user module"""

from dataclasses import fields
from rest_framework import serializers
from user.models import UserModel, UserPaymentDetailsModel, UserSubscriptionDetailsModel
from django.contrib.auth import password_validation


class UserSignUpSerializer(serializers.ModelSerializer):
    """Serializer for User sign up details"""

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = UserModel
        exclude = ["created_at","updated_at","joining_date"]

    def validate_password(self, value):
        """Function for password validation"""
        password_validation.validate_password(value, self.instance)
        return value

class UserSignInSerializer(serializers.ModelSerializer):
    """Serializer for User sign in details"""
    username = serializers.CharField()
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = UserModel
        fields = ["password","username"]

class AddNewPaymentSerializer(serializers.ModelSerializer):
    """Serializer for adding new payment details"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = UserPaymentDetailsModel
        exclude = ["created_at","updated_at"]

class AddUserSubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for adding new subscription details of a user"""
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