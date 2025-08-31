# listings/serializers.py
"""
Serializers for the listings app
"""
from rest_framework import serializers
from .models import Listing, Payment
from bookings.models import Booking
from users.serializers import UserDetailSerializer
# from addresses.serializers import AddressDetailSerializer
from reviews.serializers import ReviewDetailSerializer
# from bookings.serializers import BookingSerializer

field_list = [
    'id',
    'title',
    'description',
    'price',
    'bedrooms',
    'owner', # UserDetailSerializer
    'address', 
    'status',
    # 'reviews', # ReviewDetailSerializer
    'created_at',
]
class ListingSerializer(serializers.ModelSerializer):
    """
    Serializer for the listing
    """
    # reviews = ReviewDetailSerializer(many=True, read_only=True)
    # reviews_count = serializers.SerializerMethodField(read_only=True)

    def get_reviews_count(self, obj):
        """
        Get the number of reviews for the listing
        """
        return obj.reviews.count()
    
    
    class Meta:
        model = Listing
        # read_only_fields = ['reviews', 'reviews_count']
        fields = [*field_list]

class ListingBookingSerializer(serializers.ModelSerializer):
    """
    Serializer for the listing booking
    """
    class Meta:
        model = Booking
        fields = ['id', 'listing', 'user', 'check_in', 'check_out', 'status']
class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for the booking
    """
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'listing', 'user', 'check_in', 'check_out', 'status', 'total_price']

class ListingDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the listing detail
    """
    owner = UserDetailSerializer(read_only=True)
    # address = AddressDetailSerializer(read_only=True)

    class Meta:
        model = Listing
        fields = field_list
        depth = 1
        # read_only_fields = ['reviews', 'reviews_count']

class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for the payment
    """
    booking = BookingSerializer(read_only=True)
    class Meta:
        model = Payment
        fields = ['id', 'listing', 'amount', 'status', 'method', 'created_at', 'booking']


class PaymentInitiateSerializer(serializers.Serializer):
    """
    Serializer for the payment initiate
    """
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone = serializers.CharField()
    # tx_ref = serializers.CharField()
    booking_id = serializers.IntegerField()