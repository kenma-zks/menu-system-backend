from django.contrib import admin
from .models import FoodCategory, FoodDetails
# Register your models here.

admin.site.register(FoodCategory)
admin.site.register(FoodDetails)