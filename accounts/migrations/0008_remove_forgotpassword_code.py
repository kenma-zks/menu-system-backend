# Generated by Django 4.1.3 on 2023-04-08 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_forgotpassword_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forgotpassword',
            name='code',
        ),
    ]