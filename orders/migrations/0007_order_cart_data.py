# Generated by Django 4.1.3 on 2023-05-02 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_order_table_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cart_data',
            field=models.TextField(blank=True, null=True),
        ),
    ]