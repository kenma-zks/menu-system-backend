from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from faker import Faker

def validate_date(booking_date):
    if booking_date < timezone.now().date():
        raise ValidationError("Date cannot be in the past")

def validate_phone_number(phone_number):
    if phone_number < 9800000000 or phone_number > 9899999999:
        raise ValidationError("Please enter a valid phone number")

class Customer(models.Model):
    id = models.AutoField(primary_key= True)
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(('email address'), blank=False, null=False)
    phone_number = models.IntegerField(
        unique=True, blank=False, null=False,
        validators=[validate_phone_number]
    )
    table_capacity = models.CharField(max_length=200, blank=False, null=False)
    booking_date = models.DateField(null=True, blank=True, validators=[validate_date])
    booking_time = models.CharField(max_length=200,blank=False, null=False)
    note = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True, default="Pending")

    def __str__(self):
        return self.first_name
    
    def generate_fake_data(self):
        fake = Faker()
        self.first_name = fake.first_name()
        self.last_name = fake.last_name()
        self.email = fake.email()
        self.phone_number = fake.random_int(min=9800000000, max=9899999999)
        self.table_capacity = fake.random_element(elements=('2', '4', '6', '8'))
        self.booking_date = fake.date_between(start_date='today', end_date='+30d')
        self.booking_duration = fake.random_element(elements=('1 hour', '2 hours', '3 hours'))
        self.note = fake.sentence(nb_words=10)
        self.status = fake.random_element(elements=('Pending', 'Accepted', 'Rejected'))