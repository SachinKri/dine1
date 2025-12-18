from django.db import models


class Rider(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "delivery_rider"


class DeliveryAssignment(models.Model):
    STATUS_CHOICES = (
        ("ASSIGNED", "Assigned"),
        ("PICKED", "Picked"),
        ("DELIVERED", "Delivered"),
    )

    id = models.BigAutoField(primary_key=True)
    order_id = models.BigIntegerField()
    rider_id = models.BigIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "delivery_assignment"
        indexes = [models.Index(fields=["order_id"])]
