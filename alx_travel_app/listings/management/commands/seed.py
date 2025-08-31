# listings/management/commands/seed.py
"""
Seed the listings app
"""
from django.core.management.base import BaseCommand
from listings.models import Listing, ListingStatus
from users.models import User, UserRole
from addresses.models import Address, AddressStatus
from reviews.models import Review
from django.contrib.auth.hashers import make_password
from faker import Faker
import random

class Command(BaseCommand):
    """
    Command to seed the listings app
    """
    help = 'Seed the listings app'

    def handle(self, *args, **kwargs):
        self.fake = Faker()
        self.stdout.write('Starting to seed data...')
        
        # Clear existing data
        Review.objects.all().delete()
        Listing.objects.all().delete()
        Address.objects.all().delete()
        User.objects.all().delete()
        
        # Seed in order of dependencies
        users = self.seed_users()
        addresses = self.seed_addresses(users)
        self.update_users_with_addresses(users, addresses)
        listings = self.seed_listings(users, addresses)
        self.seed_reviews(listings, users)
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded all data!'))

    def seed_users(self):
        """
        Seed the users app with 10 users (without addresses initially)
        """
        users = []
        roles = [UserRole.USER, UserRole.REALTOR, UserRole.ADMIN]
        
        for i in range(10):
            user = User.objects.create(
                first_name=self.fake.first_name(),
                last_name=self.fake.last_name(),
                email=self.fake.unique.email(),
                password=make_password('password123'),
                phone_number=self.fake.phone_number(),
                role=random.choice(roles),
                address_id=None  # Will be updated later
            )
            users.append(user)
        
        self.stdout.write(f'Created {len(users)} users')
        return users

    def seed_addresses(self, users):
        """
        Seed the addresses app with 10 addresses
        """
        addresses = []
        
        for i in range(10):
            address = Address.objects.create(
                street=self.fake.street_address(),
                city=self.fake.city(),
                state=self.fake.state_abbr(),
                zipcode=self.fake.zipcode(),
                country=self.fake.country(),
                owner_id=users[i],
                status=AddressStatus.ACTIVE
            )
            addresses.append(address)
        
        self.stdout.write(f'Created {len(addresses)} addresses')
        return addresses

    def update_users_with_addresses(self, users, addresses):
        """
        Update users with their addresses
        """
        for i, user in enumerate(users):
            user.address_id = addresses[i]
            user.save()
        
        self.stdout.write(f'Updated {len(users)} users with addresses')

    def seed_listings(self, users, addresses):
        """
        Seed the listings app with 10 listings
        """
        listings = []
        listing_titles = [
            'Cozy Downtown Apartment', 'Modern Family Home', 'Luxury Condo with View',
            'Charming Townhouse', 'Investment Property', 'Waterfront Villa',
            'Starter Home', 'Penthouse Suite', 'Garden Cottage', 'Executive Mansion'
        ]
        
        statuses = [ListingStatus.ACTIVE, ListingStatus.INACTIVE, ListingStatus.SOLD, ListingStatus.RENTED]
        
        for i in range(10):
            listing = Listing.objects.create(
                title=listing_titles[i],
                description=self.fake.text(max_nb_chars=200),
                owner_id=users[i],
                price=random.randint(150000, 3000000),
                address_id=addresses[i],
                bedrooms=random.randint(1, 6),
                status=random.choice(statuses)
            )
            listings.append(listing)
        
        self.stdout.write(f'Created {len(listings)} listings')
        return listings

    def seed_reviews(self, listings, users):
        """
        Seed the reviews app with 10 reviews
        """
        reviews = []
        review_comments = [
            'Excellent property! Highly recommended.',
            'Great location and good value for money.',
            'Beautiful home with amazing amenities.',
            'Nice place but needs some updates.',
            'Good investment opportunity.',
            'Stunning views and luxurious finishes.',
            'Perfect for families, great neighborhood.',
            'Absolutely love this property!',
            'Charming and well-maintained.',
            'Exceptional property with premium features.'
        ]
        
        for i in range(10):
            # Use different users for reviews to avoid self-reviews
            reviewer = users[(i + 1) % len(users)]  # Cycle through users
            review = Review.objects.create(
                listing_id=listings[i],
                reviewer_id=reviewer,
                rating=random.randint(1, 5),
                comment=review_comments[i]
            )
            reviews.append(review)
        
        self.stdout.write(f'Created {len(reviews)} reviews')
        return reviews