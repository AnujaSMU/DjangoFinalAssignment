from django.db import models

# Create your models here.
class Hotel(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    price = models.IntegerField()
    available = models.BooleanField(null=True)

    def __str__(self):
        return self.name 