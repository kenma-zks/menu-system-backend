from .serializers import UserSerializer
from .models import Customer
from rest_framework import generics

class ListRegisterView(generics.ListAPIView):
  queryset = Customer.objects.all()
  serializer_class = UserSerializer

#Class based view to register user
class RegisterView(generics.CreateAPIView):
  queryset = Customer.objects.all()
  serializer_class = UserSerializer

class BookingDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Customer.objects.all()
  serializer_class = UserSerializer
