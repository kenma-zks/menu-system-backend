from django.shortcuts import render
from rest_framework import generics
from .serializers import OrderSerializer, OrderedItemSerializer
from .models import Order, OrderedItem


# Create your views here.

class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
class OrderedItemList(generics.ListCreateAPIView):
    queryset = OrderedItem.objects.all()
    serializer_class = OrderedItemSerializer

class OrderedItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderedItem.objects.all()
    serializer_class = OrderedItemSerializer