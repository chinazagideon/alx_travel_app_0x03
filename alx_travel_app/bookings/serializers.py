# bookings/serializers.py
"""
Serializers for the bookings app
"""
from rest_framework import serializers
from .models import Booking
from listings.serializers import ListingSerializer
from users.serializers import UserSerializer

class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for the booking booking
    """
    def get_total_price(self, obj):
        """
        Get the total price for the booking
        """
        return obj.listing.price * (obj.check_out - obj.check_in).days
    
    listing = ListingSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    total_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'listing', 'user', 'check_in', 'check_out', 'status', 'total_price']

class BookingDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the booking detail
    """
    listing = ListingSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    total_price = serializers.SerializerMethodField(read_only=True)

    def get_total_price(self, obj):
        """
        Get the total price for the booking
        """
        return obj.listing.price * (obj.check_out - obj.check_in).days
    
    class Meta:
        model = Booking
        fields = ['id', 'listing', 'user', 'check_in', 'check_out', 'status', 'total_price']
        depth = 1