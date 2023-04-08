from django.db import models
from menu.models import FoodDetails

# Create your models here.
class OrderedItem(models.Model):
    food_id = models.ForeignKey(FoodDetails, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return str(self.food.food_name)
    
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    items = models.ManyToManyField(OrderedItem)
    total_price = models.PositiveIntegerField()
    total_items = models.PositiveIntegerField()
    order_status = models.CharField(default='Pending', max_length=255)
    ordered_date = models.DateField(auto_now_add=True)
    ordered_time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order_id)

    
