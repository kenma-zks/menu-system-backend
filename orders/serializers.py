from rest_framework import serializers
from .models import OrderedItem, Order

class OrderedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedItem
        fields = ['food_id', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderedItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ['user_name', 'table_no', 'order_id', 'items', 'total_price', 'total_items', 'payment_method', 'order_status', 'ordered_date', 'ordered_time']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            item = OrderedItem.objects.create(**item_data)
            order.items.add(item)

        order.save()
        return order



    

    