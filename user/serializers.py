"""Serializer for user module"""

from dataclasses import fields
from rest_framework import serializers
from user.models import UserModel
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
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = UserModel
        fields = ["mobile_number","password"]
