from django.shortcuts import render
from rest_framework import generics
from .serializers import TableSerializer
from .models import Table
# Create your views here.
class TableList(generics.ListCreateAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

class TableDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer