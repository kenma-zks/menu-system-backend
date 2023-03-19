# Generated by Django 4.1.3 on 2023-03-15 09:41

import booking.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('phone_number', models.IntegerField(unique=True, validators=[booking.models.validate_phone_number])),
                ('table_capacity', models.IntegerField(default=1, validators=[booking.models.validate_table_capacity])),
                ('booking_date', models.DateField(validators=[booking.models.validate_date])),
                ('booking_duration', models.CharField(max_length=200)),
                ('note', models.CharField(blank=True, max_length=500, null=True)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
    ]
