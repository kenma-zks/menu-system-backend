from rest_framework import serializers
from .models import OrderedItem, Order

class OrderedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedItem
        fields = ['food_id', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderedItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['order_id', 'items', 'total_price', 'total_items', 'payment_method', 'order_status', 'ordered_date', 'ordered_time']

    def get_items(self, obj):
        items = OrderedItem.objects.filter(order_id=obj)
        if items:
            return OrderedItemSerializer(items, many=True).data

    

    