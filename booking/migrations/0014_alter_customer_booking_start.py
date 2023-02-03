# Generated by Django 4.1.3 on 2023-02-03 11:52

import booking.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0013_alter_customer_booking_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='booking_start',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 2, 3, 11, 52, 2, 337766, tzinfo=datetime.timezone.utc), null=True, validators=[booking.models.validate_date]),
        ),
    ]
