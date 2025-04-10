from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Hotel
from .serializers import HotelSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

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
