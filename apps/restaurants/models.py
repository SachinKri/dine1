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
