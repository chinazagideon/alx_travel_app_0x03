# listings/models.py
"""
Models for the listings app
"""
from django.db import models
from payments.models import PaymentStatus, PaymentMethod, Booking


class ListingStatus(models.TextChoices):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    SOLD = 'sold'
    RENTED = 'rented'

# Create your models here.
class Listing(models.Model):
    """
    Model for a listing
    """
    title = models.CharField(max_length=150, null=False, blank=False)
    description = models.TextField(blank=True)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)
    price = models.IntegerField(null=False, blank=False)
    address = models.CharField(max_length=150, null=False, blank=False)
    bedrooms = models.IntegerField(null=False, blank=False)
    status = models.CharField(max_length=100, choices=ListingStatus.choices, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Payment(models.Model):
    """
    Model for a payment
    """
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices)
    transaction_id = models.CharField(max_length=100)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    