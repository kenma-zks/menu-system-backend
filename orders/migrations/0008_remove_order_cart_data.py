# Generated by Django 4.1.3 on 2023-05-02 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_order_cart_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cart_data',
        ),
    ]
