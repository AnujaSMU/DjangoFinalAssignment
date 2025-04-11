from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Hotel, Guest, Reservation
from .serializers import HotelSerializer, GuestSerializer, ReservationInputSerializer, ReservationResponseSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
import uuid
from django.db.models import Q
from datetime import datetime

# Create your views here.
@csrf_exempt
def Hotels_list(request):
    if request.method == 'GET':
        hotels = Hotel.objects.all()
        serializer = HotelSerializer(hotels, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = HotelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def Hotels_detail(request, id):
    try:
        hotel = Hotel.objects.get(id=id)
    except Hotel.DoesNotExist:
        return JsonResponse({'error': 'Hotel not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = HotelSerializer(hotel)
        return JsonResponse(serializer.data)

class get_generics_list(generics.ListCreateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

@csrf_exempt
def reservationConfirmation(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        input_serializer = ReservationInputSerializer(data=data)
        
        if input_serializer.is_valid():
            # Create a new reservation
            reservation = Reservation.objects.create(
                hotel_name=input_serializer.validated_data['hotel_name'],
                checkin=input_serializer.validated_data['checkin'],
                checkout=input_serializer.validated_data['checkout'],
            )
            
            # Create and add guests to the reservation
            for guest_data in input_serializer.validated_data['guests_list']:
                guest = Guest.objects.create(
                    guest_name=guest_data['guest_name'],
                    gender=guest_data['gender']
                )
                reservation.guests.add(guest)
            
            # Return the confirmation number
            response_serializer = ReservationResponseSerializer(reservation)
            return JsonResponse(response_serializer.data, status=status.HTTP_201_CREATED)
            
        return JsonResponse(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    return JsonResponse({'error': 'Only POST method is allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@csrf_exempt
def available_hotels(request):
    if request.method == 'GET':
        checkin = request.GET.get('checkin', None)
        checkout = request.GET.get('checkout', None)
        
        if not checkin or not checkout:
            return JsonResponse(
                {'error': 'Both checkin and checkout dates are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Try to parse dates in MM/DD/YYYY format first
            try:
                checkout_date = datetime.strptime(checkout, '%m/%d/%Y').date()
            except ValueError:
                # Fallback to YYYY-MM-DD format
                checkout_date = datetime.strptime(checkout, '%Y-%m-%d').date()
            
            # Find hotels available until checkout date
            available_hotels = Hotel.objects.filter(
                available_until__gte=checkout_date,
                available=True
            )
            
            serializer = HotelSerializer(available_hotels, many=True)
            return JsonResponse(serializer.data, safe=False)
            
        except ValueError:
            return JsonResponse(
                {'error': 'Invalid date format. Use MM/DD/YYYY or YYYY-MM-DD'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    return JsonResponse(
        {'error': 'Only GET method is allowed'}, 
        status=status.HTTP_405_METHOD_NOT_ALLOWED
    )
