from django.db import models


class NotificationLog(models.Model):
    CHANNEL_CHOICES = (
        ("EMAIL", "Email"),
        ("SMS", "SMS"),
        ("PUSH", "Push"),
    )

    id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField(null=True)
    channel = models.CharField(max_length=10, choices=CHANNEL_CHOICES)
    message = models.TextField()

    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notifications_log"
        indexes = [models.Index(fields=["user_id"])]
