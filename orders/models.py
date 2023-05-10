from django.db import models
from menu.models import FoodDetails

# Create your models here.
class OrderedItem(models.Model):
    food_id = models.ForeignKey(FoodDetails, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return str(self.food_id.food_name)
    
class Order(models.Model):
    user_name = models.CharField(max_length=255, blank=True, null=True)
    table_no = models.CharField(max_length=255, blank=True, null=True)
    order_id = models.AutoField(primary_key=True)
    items = models.ManyToManyField(OrderedItem)
    total_price = models.PositiveIntegerField()
    total_items = models.PositiveIntegerField()
    note = models.CharField(max_length=255, blank=True, null=True)
    payment_method = models.CharField(max_length=128, blank=True, null=True)
    order_status = models.CharField(default='Pending', max_length=255)
    ordered_date = models.DateField(auto_now_add=True)
    ordered_time = models.TimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=128, blank=True, null=True)
    payment_amount = models.PositiveIntegerField(blank=True, null=True)
    payment_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.user_name)
    

    
