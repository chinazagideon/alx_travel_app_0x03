# bookings/models.py
"""
Models for the bookings app
"""
from django.db import models
from django.conf import settings
from users.models import User
from decimal import Decimal

class BookingStatus(models.TextChoices):
    """
    Booking status choices
    """
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'
    PENDING_PAYMENT = 'pending_payment'
    PAID = 'paid'
    REFUNDED = 'refunded'
    EXPIRED = 'expired'
    CANCELLED_BY_USER = 'cancelled_by_user'

class Booking(models.Model):
    """
    Booking model
    """

    

    listing = models.ForeignKey(settings.AUTH_LISTING_MODEL, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=BookingStatus.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Automatically compute total_price from listing.price and stay duration
        if self.listing_id and self.check_in and self.check_out:
            num_nights = (self.check_out - self.check_in).days
            if num_nights < 0:
                num_nights = 0
            self.total_price = Decimal(str(self.listing.price)) * Decimal(num_nights)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.listing.title}"