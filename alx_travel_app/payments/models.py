from django.db import models
from bookings.models import Booking
# from listings.models import Listing
from django.conf import settings
# Create your models here.
class PaymentStatus(models.TextChoices):
    """
    Payment status choices
    """
    PENDING = 'pending'
    SUCCESSFUL = 'successful'
    FAILED = 'failed'
    REFUNDED = 'refunded'
    CANCELLED = 'cancelled'

class PaymentMethod(models.TextChoices):
    """
    Payment method choices
    """
    CREDIT_CARD = 'credit_card'
    DEBIT_CARD = 'debit_card'
    PAYPAL = 'paypal'
    STRIPE = 'stripe'
    CASH = 'cash'
# class Payment(models.Model):
#     """
#     Model for a payment
#     """
#     listing = models.ForeignKey(settings.AUTH_LISTING_MODEL, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=20, choices=PaymentStatus.choices)
#     transaction_id = models.CharField(max_length=100)
#     booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
#     method = models.CharField(max_length=20, choices=PaymentMethod.choices)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)    