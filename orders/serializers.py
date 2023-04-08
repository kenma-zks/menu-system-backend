from rest_framework import serializers
from .models import OrderedItem, Order

class OrderedItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderedItem
        fields = ('food_id', 'quantity')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderedItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('order_id', 'items', 'total_price', 'total_items', 'order_status', 'ordered_date', 'ordered_time')
    
    def create(self, validated_data):
        items = validated_data.pop('items', [])
        print(items)
        order = Order.objects.create(**validated_data)
        for item in items:
            order.items.add(item)
        return order

    