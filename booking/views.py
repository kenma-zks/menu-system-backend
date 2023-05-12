from .serializers import UserSerializer
from .models import Customer
from rest_framework import generics
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

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

@csrf_exempt
@api_view(['POST'])
def send_email(request):
  email = request.data.get('email')
  status = request.data.get('status')
  booking_time = request.data.get('booking_time')
  booking_date = request.data.get('booking_date')
  table_capacity = request.data.get('table_capacity')

  print(email)

  if status == 'Accepted':
    send_mail (
      'Booking Accepted',
      'Your booking has been accepted, We are looking forward to see you. \n\nBooking Details: \nDate: ' + booking_date + '\nTime: ' + booking_time + '\nTable Capacity: ' + table_capacity,
      settings.EMAIL_HOST_USER,
      [email],
      fail_silently=False,
    )
  elif status == 'Rejected':
    send_mail (
      'Booking Rejected',
      'Your booking has been rejected, We are sorry for the inconvenience.',
      settings.EMAIL_HOST_USER,
      [email],
      fail_silently=False,
    )

  return Response({'message': 'Email sent successfully'}, status=200)

