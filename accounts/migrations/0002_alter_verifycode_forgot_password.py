# Generated by Django 4.1.3 on 2023-04-09 04:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verifycode',
            name='forgot_password',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.forgotpassword'),
        ),
        migrations.AddField(
            model_name='verifycode',
            name='forgot_password',
            field=models.ForeignKey(
                to='accounts.ForgotPassword',
                on_delete=models.CASCADE
            ),
        ),
    ]
