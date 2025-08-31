# reviews/serializers.py
"""
Serializers for the reviews app
"""
from rest_framework import serializers
from .models import Review
from users.serializers import UserDetailSerializer
# from .serializers import ListingDetailSerializer

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the review
    """
    reviewer = UserDetailSerializer(read_only=True)
    listing = "listings.ListingDetailSerializer"

    def validate_rating(self, value):
        """
        Validate the rating
        """
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value
    class Meta:
        model = Review
        fields = ['id', 'rating', 'comment', 'created_at', 'updated_at']

class ReviewDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the review detail
    """
    reviewer = UserDetailSerializer(read_only=True)
    # listing = ListingDetailSerializer(read_only=True)
    listing = "listings.ListingDetailSerializer"


    def validate_rating(self, value):
        """
        Validate the rating
        """
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value

    class Meta:
        model = Review
        fields = ['id', 'rating', 'comment', 'created_at', 'updated_at']
        depth = 1