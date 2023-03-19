from .serializers import UserSerializer
from .models import Customer
from rest_framework import generics
from django.utils import timezone

class ListRegisterView(generics.ListAPIView):
  queryset = Customer.objects.filter(booking_date__gte=timezone.now().date())
  serializer_class = UserSerializer

class ListPastRegisterView(generics.ListAPIView):
  queryset = Customer.objects.filter(booking_date__lt=timezone.now().date())
  serializer_class = UserSerializer

#Class based view to register user
class RegisterView(generics.CreateAPIView):
  queryset = Customer.objects.all()
  serializer_class = UserSerializer

class BookingDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Customer.objects.all()
  serializer_class = UserSerializer

class PastBookingDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Customer.objects.all()
  serializer_class = UserSerializer
