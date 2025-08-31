"""
Listing URLs
"""

from django.urls import path, include
from rest_framework import routers
from .views import BookingViewSet, ListingViewSet, PaymentViewSet
from users.views import UserViewSet
# from addresses.views import AddressView
from rest_framework import routers
# from rest_framework_nested import routers as nested_routers
from rest_framework.authtoken import views as auth_views

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'listings', ListingViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'payments', PaymentViewSet)

# urlpatterns = [
#     #api
#     path('', include(router.urls)),

#     path('auth/', auth_views.obtain_auth_token),
# ]

urlpatterns = router.urls