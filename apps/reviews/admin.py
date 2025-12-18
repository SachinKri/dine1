from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "restaurant_id", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("restaurant_id", "user_id")
    readonly_fields = ("created_at",)
