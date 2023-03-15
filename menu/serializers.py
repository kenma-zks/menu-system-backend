from rest_framework import serializers
from .models import  FoodCategory, FoodDetails

class FoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = ('id','category_name',)

class FoodDetailsSerializer(serializers.ModelSerializer):
    food_image = serializers.ImageField(required=False)
    class Meta:
        model = FoodDetails
        fields = ('id','category_id', 'food_name', 'food_price', 'food_description', 'food_image', 'food_available')
    