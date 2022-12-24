from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_date(booking_start):
    if booking_start < timezone.now():
        raise ValidationError("Date cannot be in the past")  

def validate_phone_number(phone_number):
    if phone_number < 9800000000 or phone_number > 9899999999:
        raise ValidationError("Please enter a valid phone number")

def validate_table_capacity(table_capacity):
    if table_capacity < 1 or table_capacity > 12:
        raise ValidationError("Please enter a valid table capacity")

# class Table(models.Model):
#     table_id = models.AutoField(primary_key= True)
#     table_capacity = models.IntegerField(blank=False, null=False)
#     table_status = models.BooleanField(default=False)
#     table_note = models.CharField(max_length=500, blank=True, null=True)
#     booking_duration = models.CharField(max_length=200,blank=False, null=False)


#     def __str__(self):
#         return str(self.table_id)


class Customer(models.Model):
    id = models.AutoField(primary_key= True)
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(('email address'), unique=True, blank=False, null=False)
    phone_number = models.IntegerField(
        unique=True, blank=False, null=False,
        validators=[validate_phone_number]
    )
    table_capacity = models.IntegerField(blank=False, null=False, default=1, validators=[validate_table_capacity])
    booking_start = models.DateTimeField(null=True, blank=True, default = timezone.now() , validators=[validate_date])
    booking_duration = models.CharField(max_length=200,blank=False, null=False)
    note = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.first_name


