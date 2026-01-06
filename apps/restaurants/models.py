'''
from django.db import models
class Restaurant(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    city = models.CharField(max_length=100)
    is_open = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "restaurants_restaurant"


class MenuItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    restaurant_id = models.BigIntegerField()
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "restaurants_menu_item"
        indexes = [models.Index(fields=["restaurant_id"])]
'''

from django.db import models
import uuid

# Restaurant Model
class Restaurant(models.Model):
    id = models.UUIDField(primary_key=True, 
                          default=uuid.uuid4, 
                          editable=False)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    address = models.TextField()

    owner_id = models.UUIDField()  # Logical reference to Users service

    is_open = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Menu Category Model
class MenuCategory(models.Model):
    id = models.UUIDField(primary_key=True, 
                          default=uuid.uuid4, 
                          editable=False)

    restaurant_id = models.UUIDField()  # Logical reference
    name = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# Menu Item Model
class MenuItem(models.Model):
    id = models.UUIDField(primary_key=True, 
                          default=uuid.uuid4, 
                          editable=False)

    category_id = models.UUIDField()  # Logical reference
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
