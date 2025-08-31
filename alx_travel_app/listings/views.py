import requests
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

CHAPA_TEST_SECRET_KEY = os.getenv("CHAPA_TEST_SECRET_KEY")

from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status
from bookings.models import Booking
from .models import Listing, Payment, PaymentStatus
from django.conf import settings
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import logging
from .serializers import PaymentSerializer, ListingSerializer
from bookings.serializers import BookingSerializer
from rest_framework.views import APIView
from django.urls import reverse
from .serializers import (
    ListingSerializer,
    BookingSerializer,
    PaymentSerializer,
    PaymentInitiateSerializer,
)
from .tasks import send_booking_email_notification, send_booking_confirmation_email


class ListingViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing Listing
    """

    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing Bookings
    """

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a booking
        """
        serializer = BookingSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated = serializer.validated_data
        listing = validated.get("listing")
        check_in = validated.get("check_in")
        check_out = validated.get("check_out")

        num_nights = (check_out - check_in).days if (check_in and check_out) else 0
        if num_nights < 0:
            num_nights = 0
        total_price = listing.price * num_nights if listing else 0

        booking = serializer.save(total_price=total_price)

        # Send booking confirmation email
        send_booking_confirmation_email.delay(booking.reference, booking.email)
        # Return the created booking data
        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)



class PaymentViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing Payments
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class InitiatePaymentView(APIView):
    """
    API endpoint for initiating a payment
    """

    def post(self, request, *args, **kwargs):
        """
        Initiate a payment
        """

        serializer = PaymentInitiateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # else:

            # return Response(serializer.data, status=status.HTTP_200_OK)
        
        # get request data
        url = "https://api.chapa.co/v1/transaction/initialize"

        headers = {
            "Authorization": f"Bearer {CHAPA_TEST_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        tx_ref = str(uuid.uuid4())
        callback_url = 'https://127.0.0.1:8000/api/pay/verify-payment/'

        booking = Booking.objects.get(id=request.data.get("booking_id"))

        data = {
            "amount": request.data.get("amount"),
            "currency": "ETB",
            "booking_id": booking.id,
            "email": request.data.get("email"),
            "first_name": request.data.get("first_name"),
            "last_name": request.data.get("last_name"),
            "phone": request.data.get("phone"),
            "tx_ref": tx_ref,
            "callback_url": callback_url,
            "return_url": callback_url,
        }
        try:
            response = requests.post(
                url, headers=headers, json=data, timeout=settings.CHAPA_TIMEOUT
            )
        except requests.exceptions.Timeout:
            return Response(
                {"error": "Request timed out"}, status=status.HTTP_504_GATEWAY_TIMEOUT
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if response.status_code == status.HTTP_200_OK:
            payment_url = response.json().get("data", {}).get("checkout_url")
            return Response({"payment_url": payment_url, "tx_ref": tx_ref}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": response.json()}, status=status.HTTP_400_BAD_REQUEST
            )


class VerifyPaymentView(APIView):
    """
    API endpoint for verifying a payment
    """

    def get(self, request, *args, **kwargs):
        """
        Verify a payment
        """
        # get transaction id from query params
        tx_ref = request.query_params.get("tx_ref")

        if not tx_ref:
            return Response(
                {"error": "Transaction reference is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # make request to chapa to verify payment
        url = f"https://api.chapa.co/v1/transaction/verify/{tx_ref}"
        headers = {
            "Authorization": f"Bearer {CHAPA_TEST_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.get(
                url, headers=headers, timeout=settings.CHAPA_TIMEOUT
            )
        except requests.exceptions.Timeout:
            return Response(
                {"error": "Request timed out"}, status=status.HTTP_504_GATEWAY_TIMEOUT
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if response.status_code == status.HTTP_200_OK:
            chapa_response = response.json()
            if chapa_response.get("status") == "success":
                # return Response(chapa_response, status=status.HTTP_200_OK)
                
                # find payment modal instance
                payment = Payment.objects.filter(tx_ref=tx_ref)
                try:
                    if payment:
                        try:
                            send_booking_email_notification.delay(
                            payment.booking.reference, payment.booking.email
                            )
                        except Exception as e:
                            return Response(
                                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
                            )
                        payment.status = PaymentStatus.SUCCESSFUL
                        # payment.save() # update payment status to successful, and update booking status to paid
                        return Response(
                            {"message": "Payment verified successfully"},
                            status=status.HTTP_200_OK,
                        )
                    else:
                        return Response(
                            {"error": "error-001: Payment not found"},
                            status=status.HTTP_404_NOT_FOUND,
                        )
                except Payment.DoesNotExist:
                    return Response(
                        {"error": "error-001: Payment not found"}, status=status.HTTP_404_NOT_FOUND
                    )
            else:
                try:
                    payment = Payment.objects.filter(transaction_id=tx_ref)
                    if payment:
                        payment.status = PaymentStatus.FAILED
                        payment.save()
                        return Response(
                            {"error": "Payment failed"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                except Payment.DoesNotExist:
                    return Response(
                        {"error": "error-002: Payment not found"}, status=status.HTTP_404_NOT_FOUND
                    )
        else:
            return Response(
                {"error": response.json()}, status=status.HTTP_400_BAD_REQUEST
            )
