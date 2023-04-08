# Generated by Django 4.1.3 on 2023-04-07 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderedItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.fooddetails')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('total_price', models.PositiveIntegerField()),
                ('total_items', models.PositiveIntegerField()),
                ('order_status', models.CharField(default='Pending', max_length=255)),
                ('ordered_date', models.DateField(auto_now_add=True)),
                ('ordered_time', models.TimeField(auto_now_add=True)),
                ('items', models.ManyToManyField(to='orders.ordereditem')),
            ],
        ),
    ]