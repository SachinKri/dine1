from django.db import models


class Transaction(models.Model):
    PAYMENT_MODE_CHOICES = (
        ("UPI", "UPI"),
        ("CARD", "Card"),
        ("WALLET", "Wallet"),
        ("COD", "Cash on Delivery"),
    )

    STATUS_CHOICES = (
        ("INITIATED", "Initiated"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
        ("REFUNDED", "Refunded"),
    )

    id = models.BigAutoField(primary_key=True)
    order_id = models.BigIntegerField()
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_MODE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    gateway_reference = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "payments_transaction"
        indexes = [models.Index(fields=["order_id"])]
