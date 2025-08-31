# users/serializers.py
"""
Serializers for the users app
"""
from rest_framework import serializers
# from .models import User
from django.contrib.auth import get_user_model

User = get_user_model()



class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the user
    """
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password','phone_number', 'role', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create_user(self, validated_data):
        """
        Override the default create method handle user signup
        """

        user = User.objects.create_user(**validated_data)
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the user detail
    """
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at', 'updated_at']