from django.db import models

# Create your models here.
class FoodCategory(models.Model):
    # Represents a food category
    category_name = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        verbose_name_plural = "Food Category"

    def __str__(self):
        return self.category_name

# def upload_to(instance, filename):
#     return 'images/{filename}'.format(filename=filename)

class FoodDetails(models.Model):
    category_id = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, related_name='category_id')
    food_name = models.CharField(max_length=255, blank=False, null=False)
    food_price = models.IntegerField(blank=False, null=False)
    food_description = models.CharField(max_length=255, blank=False, null=False)
    food_image = models.ImageField(upload_to='food_images', blank=True, null=True)
    food_available = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Food Details"

    def __str__(self):
        return self.food_name
