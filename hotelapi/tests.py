from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import json
from datetime import datetime, date, timedelta
from .models import Hotel, Guest, Reservation

# Create your tests here.
class HotelAPITestCase(TestCase):
    def setUp(self):
        # Set up test client
        self.client = APIClient()
        
        # Create test hotels
        self.hotel1 = Hotel.objects.create(
            id=1,
            name="Test Hotel 1",
            rating=4.5,
            price=150,
            available_until=date.today() + timedelta(days=30),
            available=True
        )
        
        self.hotel2 = Hotel.objects.create(
            id=2,
            name="Test Hotel 2",
            rating=3.5,
            price=100,
            available_until=date.today() + timedelta(days=10),
            available=True
        )
        
        self.hotel3 = Hotel.objects.create(
            id=3,
            name="Test Hotel 3",
            rating=5.0,
            price=200,
            available_until=date.today() - timedelta(days=5),  # Not available (past date)
            available=True
        )
        
        self.hotel4 = Hotel.objects.create(
            id=4,
            name="Test Hotel 4",
            rating=4.0,
            price=120,
            available_until=date.today() + timedelta(days=20),
            available=False  # Not available (flag is False)
        )

    def test_hotels_list_get(self):
        """Test GET request to Hotels_list endpoint retrieves all hotels"""
        url = reverse('hotelList')  # Using correct URL name from urls.py
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 4)  # Should return all 4 hotels
        
        # Verify hotel details
        hotels_data = response.json()
        hotel_ids = [hotel['id'] for hotel in hotels_data]
        self.assertIn(1, hotel_ids)
        self.assertIn(2, hotel_ids)
        self.assertIn(3, hotel_ids)
        self.assertIn(4, hotel_ids)

    def test_hotels_list_post(self):
        """Test POST request to Hotels_list endpoint creates a new hotel"""
        url = reverse('hotelList')  # Using correct URL name from urls.py
        
        new_hotel_data = {
            "id": 5,
            "name": "New Test Hotel",
            "rating": 4.2,
            "price": 130,
            "available_until": (date.today() + timedelta(days=15)).isoformat(),
            "available": True
        }
        
        response = self.client.post(
            url, 
            data=json.dumps(new_hotel_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify hotel was created
        created_hotel = Hotel.objects.get(id=5)
        self.assertEqual(created_hotel.name, "New Test Hotel")
        self.assertEqual(created_hotel.price, 130)

    def test_available_hotels(self):
        """Test available_hotels endpoint returns only available hotels based on date criteria"""
        # Create URL with query parameters
        tomorrow = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        next_week = (date.today() + timedelta(days=7)).strftime('%Y-%m-%d')
        
        url = f"/available_hotels/?checkin={tomorrow}&checkout={next_week}"
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Only hotels 1 and 2 should be available (hotel 3 has past date, hotel 4 has available=False)
        hotels_data = response.json()
        self.assertEqual(len(hotels_data), 2)
        
        hotel_ids = [hotel['id'] for hotel in hotels_data]
        self.assertIn(1, hotel_ids)
        self.assertIn(2, hotel_ids)
        self.assertNotIn(3, hotel_ids)
        self.assertNotIn(4, hotel_ids)
    
    def test_available_hotels_missing_parameters(self):
        """Test available_hotels endpoint returns error when parameters are missing"""
        url = reverse('availableHotels')  # Using correct URL name from urls.py
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.json())
    
    def test_reservation_confirmation(self):
        """Test reservationConfirmation endpoint creates a new reservation"""
        url = reverse('reservationConfirmation')  # Using correct URL name from urls.py
        
        reservation_data = {
            "hotel_name": "Test Hotel 1",
            "checkin": (date.today() + timedelta(days=1)).isoformat(),
            "checkout": (date.today() + timedelta(days=3)).isoformat(),
            "guests_list": [
                {
                    "guest_name": "John Doe",
                    "gender": "Male"
                },
                {
                    "guest_name": "Jane Doe",
                    "gender": "Female"
                }
            ]
        }
        
        response = self.client.post(
            url,
            data=json.dumps(reservation_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify reservation was created
        self.assertTrue('confirmation_number' in response.json())
        
        # Check if the reservation exists in the database
        confirmation_number = response.json()['confirmation_number']
        reservation = Reservation.objects.get(confirmation_number=confirmation_number)
        self.assertEqual(reservation.hotel_name, "Test Hotel 1")
        
        # Verify guests were added
        self.assertEqual(reservation.guests.count(), 2)
        guest_names = [guest.guest_name for guest in reservation.guests.all()]
        self.assertIn("John Doe", guest_names)
        self.assertIn("Jane Doe", guest_names)
    
    def test_reservation_confirmation_with_slash_dates(self):
        """Test reservationConfirmation endpoint with dates in MM/DD/YYYY format"""
        url = reverse('reservationConfirmation')  # Using correct URL name from urls.py
        
        tomorrow = (date.today() + timedelta(days=1)).strftime('%m/%d/%Y')
        checkout_date = (date.today() + timedelta(days=3)).strftime('%m/%d/%Y')
        
        reservation_data = {
            "hotel_name": "Test Hotel 1",
            "checkin": tomorrow,
            "checkout": checkout_date,
            "guests_list": [
                {
                    "guest_name": "Bob Smith",
                    "gender": "Male"
                }
            ]
        }
        
        response = self.client.post(
            url,
            data=json.dumps(reservation_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify reservation was created
        self.assertTrue('confirmation_number' in response.json())
        
    def test_reservation_confirmation_invalid_data(self):
        """Test reservationConfirmation endpoint with invalid data"""
        url = reverse('reservationConfirmation')
        
        # Missing required field (guests_list)
        reservation_data = {
            "hotel_name": "Test Hotel 1",
            "checkin": (date.today() + timedelta(days=1)).isoformat(),
            "checkout": (date.today() + timedelta(days=3)).isoformat()
        }
        
        response = self.client.post(
            url,
            data=json.dumps(reservation_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Invalid date format
        reservation_data = {
            "hotel_name": "Test Hotel 1",
            "checkin": "invalid-date",
            "checkout": (date.today() + timedelta(days=3)).isoformat(),
            "guests_list": [
                {
                    "guest_name": "Test User",
                    "gender": "Male"
                }
            ]
        }
        
        response = self.client.post(
            url,
            data=json.dumps(reservation_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
