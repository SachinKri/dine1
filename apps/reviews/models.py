from django.db import models


class Review(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField()
    restaurant_id = models.BigIntegerField()
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "reviews_review"
        indexes = [models.Index(fields=["restaurant_id"])]
