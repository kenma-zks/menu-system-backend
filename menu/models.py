from django.db import models
from faker import Faker

# Create your models here.
class FoodCategory(models.Model):
    # Represents a food category
    category_name = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        verbose_name_plural = "Food Category"

    def __str__(self):
        return self.category_name
    
    def generate_fake_data(self):
        fake = Faker()
        self.category_name = fake.random_element(elements=('Breakfast', 'Lunch', 'Dinner'))


class FoodDetails(models.Model):
    food_id = models.AutoField(primary_key=True)
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

    def generate_fake_data(self):
        fake = Faker()
        category = FoodCategory.objects.order_by('?').first()
        self.category_id = category
        self.food_name = fake.random_element(elements=('Burger', 'Pizza', 'Sandwich'))
        self.food_price = fake.random_int(min=100, max=500)
        self.food_description = fake.sentence(nb_words=10)
        self.food_image = fake.image_url(width=200, height=200)
        self.food_available = fake.boolean(chance_of_getting_true=50)


