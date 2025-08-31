# users/models.py
"""
Models for the users app
"""
from django.db import models

class UserRole(models.TextChoices):
    ADMIN = 'admin'
    USER = 'user'
    REALTOR = 'realtor'

# Create your models here.
class User(models.Model):
    """
    Model for a user
    """
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    addresses = models.ForeignKey('addresses.Address', on_delete=models.CASCADE, null=True, blank=True)
    password = models.CharField(max_length=100, null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(max_length=100, choices=UserRole.choices, null=False, blank=False)
    is_anonymous = models.BooleanField(null=True, blank=True)
    is_authenticated = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    def __str__(self):
        return self.first_name