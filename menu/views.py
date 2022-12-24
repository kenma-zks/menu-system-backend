from django.shortcuts import render
from rest_framework import generics
from .serializers import FoodDetailsSerializer, FoodCategorySerializer
from .models import FoodDetails, FoodCategory
# from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.

class FoodCategoryList(generics.ListCreateAPIView):
    queryset = FoodCategory.objects.all()
    serializer_class = FoodCategorySerializer

class FoodCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FoodCategory.objects.all()
    serializer_class = FoodCategorySerializer

class FoodDetailsList(generics.ListCreateAPIView):
    queryset = FoodDetails.objects.all()
    serializer_class = FoodDetailsSerializer
    
class FoodDetailsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FoodDetails.objects.all()
    serializer_class = FoodDetailsSerializer