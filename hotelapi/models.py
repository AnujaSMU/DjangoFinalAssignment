from django.db import models
import uuid

# Create your models here.
class Hotel(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    price = models.IntegerField()
    available_until = models.DateField()
    available = models.BooleanField(null=True)

    def __str__(self):
        return self.name 

class Guest(models.Model):
    guest_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)

    def __str__(self):
        return self.guest_name

class Reservation(models.Model):
    confirmation_number = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    hotel_name = models.CharField(max_length=100)
    checkin = models.DateField()
    checkout = models.DateField()
    guests = models.ManyToManyField(Guest)
    
    def __str__(self):
        return self.confirmation_number

