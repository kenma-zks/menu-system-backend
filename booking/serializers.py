from rest_framework import serializers
from .models import Customer
from django.utils import timezone
from django.core.exceptions import ValidationError



#Serializer to Get User Details using Django Token Authentication
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = Customer
    fields = ["id", "first_name", "last_name", "email", "phone_number", "table_capacity", "booking_date", "booking_duration", "note", "status"]

  def create(self, validated_data):
    user = Customer.objects.create(
      first_name=validated_data['first_name'],
      last_name=validated_data['last_name'],
      email=validated_data['email'],
      phone_number=validated_data['phone_number'],
      table_capacity=validated_data['table_capacity'],
      booking_date=validated_data['booking_date'],
      booking_duration=validated_data['booking_duration'],
      note=validated_data['note'],
      status=validated_data['status'],
    )
    user.save()
    return user
