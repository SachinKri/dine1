from django.db import models


class Order(models.Model):
    STATUS_CHOICES = (
        ("CREATED", "Created"),
        ("CONFIRMED", "Confirmed"),
        ("PREPARING", "Preparing"),
        ("OUT_FOR_DELIVERY", "Out for Delivery"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    )

    id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField()
    restaurant_id = models.BigIntegerField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_address = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "orders_order"
        indexes = [
            models.Index(fields=["user_id"]),
            models.Index(fields=["restaurant_id"]),
        ]


class OrderItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    order_id = models.BigIntegerField()
    menu_item_id = models.BigIntegerField()
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "orders_order_item"
        indexes = [models.Index(fields=["order_id"])]
