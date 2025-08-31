# addresses/models.py
"""
Models for the addresses app
"""
from django.db import models

class AddressStatus(models.TextChoices):
    ACTIVE = 'active'
    INACTIVE = 'inactive'

# Create your models here.
class Address(models.Model):
    """
    Model for an address
    """
    street = models.CharField(max_length=100, null=False, blank=False)
    city = models.CharField(max_length=100, null=False, blank=False)
    state = models.CharField(max_length=100, null=False, blank=False)
    zipcode = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=100, null=False, blank=False)
    owner_id = models.ForeignKey('users.User', on_delete=models.CASCADE, null=False, blank=False)
    status = models.CharField(max_length=10, choices=AddressStatus.choices, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.street