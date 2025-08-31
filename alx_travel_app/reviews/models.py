# reviews/models.py
"""
Models for the reviews app
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Constants for the rating
min_rating = 1
max_rating = 5

# Create your models here.
class Review(models.Model):
    """
    Model for a review
    """
    listing_id = models.ForeignKey('listings.Listing', on_delete=models.CASCADE)
    reviewer_id = models.ForeignKey('users.User', on_delete=models.CASCADE)
    rating = models.IntegerField(null=False, blank=False, 
                                 validators=[MinValueValidator(min_rating), MaxValueValidator(max_rating)])
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment