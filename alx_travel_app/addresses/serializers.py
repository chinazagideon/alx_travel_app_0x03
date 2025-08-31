# addresses/serializers.py
"""
Serializers for the addresses app
"""
from rest_framework import serializers
from .models import Address
from users.serializers import UserDetailSerializer

class AddressSerializer(serializers.ModelSerializer):
    """
    Serializer for the address
    """
    class Meta:
        model = Address
        fields = ['id', 'street', 'city', 'state', 'zipcode', 'country', 'owner_id', 'status', 'created_at', 'updated_at']

class AddressDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the address detail
    """
    owner = UserDetailSerializer(read_only=True)