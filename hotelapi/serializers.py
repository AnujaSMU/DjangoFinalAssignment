from rest_framework import serializers
from .models import Hotel, Guest, Reservation

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['id', 'name', 'rating', 'price', 'available_until', 'available']

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ['guest_name', 'gender']

class ReservationInputSerializer(serializers.Serializer):
    hotel_name = serializers.CharField(max_length=100)
    checkin = serializers.DateField()
    checkout = serializers.DateField()
    guests_list = GuestSerializer(many=True)

class ReservationResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['confirmation_number'] 