from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Hotel, Guest, Reservation
from .serializers import HotelSerializer, GuestSerializer, ReservationInputSerializer, ReservationResponseSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import JSONParser
import uuid
from django.db.models import Q
from datetime import datetime

# Create your views here.
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])  # In production, consider using IsAuthenticated
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

@api_view(['GET'])
@permission_classes([AllowAny])  # In production, consider using IsAuthenticated
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
    permission_classes = [AllowAny]  # In production, consider using IsAuthenticated

@api_view(['POST'])
@permission_classes([AllowAny])  # In production, consider using IsAuthenticated
def reservationConfirmation(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        
        # Convert date formats if they use slashes
        if 'checkin' in data and isinstance(data['checkin'], str) and '/' in data['checkin']:
            try:
                date_obj = datetime.strptime(data['checkin'], '%m/%d/%Y')
                data['checkin'] = date_obj.strftime('%Y-%m-%d')
            except ValueError:
                return JsonResponse(
                    {'error': 'Invalid checkin date format. Use MM/DD/YYYY'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        if 'checkout' in data and isinstance(data['checkout'], str) and '/' in data['checkout']:
            try:
                date_obj = datetime.strptime(data['checkout'], '%m/%d/%Y')
                data['checkout'] = date_obj.strftime('%Y-%m-%d')
            except ValueError:
                return JsonResponse(
                    {'error': 'Invalid checkout date format. Use MM/DD/YYYY'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
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

@api_view(['GET'])
@permission_classes([AllowAny])  # In production, consider using IsAuthenticated
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
            # Convert checkout date format if it contains slashes
            if '/' in checkout:
                try:
                    checkout_date = datetime.strptime(checkout, '%m/%d/%Y').date()
                except ValueError:
                    return JsonResponse(
                        {'error': 'Invalid checkout date format. Use MM/DD/YYYY'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                # Assume YYYY-MM-DD format
                try:
                    checkout_date = datetime.strptime(checkout, '%Y-%m-%d').date()
                except ValueError:
                    return JsonResponse(
                        {'error': 'Invalid checkout date format. Use YYYY-MM-DD'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Find hotels available until checkout date
            available_hotels = Hotel.objects.filter(
                available_until__gte=checkout_date,
                available=True
            )
            
            serializer = HotelSerializer(available_hotels, many=True)
            return JsonResponse(serializer.data, safe=False)
            
        except Exception as e:
            return JsonResponse(
                {'error': f'Error processing dates: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    return JsonResponse(
        {'error': 'Only GET method is allowed'}, 
        status=status.HTTP_405_METHOD_NOT_ALLOWED
    )

@api_view(['GET'])
@permission_classes([AllowAny])  # In production, consider using IsAuthenticated
def reservation_list(request):
    """
    Get a list of all reservations
    """
    if request.method == 'GET':
        reservations = Reservation.objects.all().prefetch_related('guests')
        
        # Create a custom response with more details than just confirmation numbers
        result = []
        for reservation in reservations:
            guests = [
                {
                    'guest_name': guest.guest_name,
                    'gender': guest.gender
                } 
                for guest in reservation.guests.all()
            ]
            
            result.append({
                'confirmation_number': reservation.confirmation_number,
                'hotel_name': reservation.hotel_name,
                'checkin': reservation.checkin,
                'checkout': reservation.checkout,
                'guests': guests
            })
            
        return JsonResponse(result, safe=False)
    
    return JsonResponse(
        {'error': 'Only GET method is allowed'}, 
        status=status.HTTP_405_METHOD_NOT_ALLOWED
    )
