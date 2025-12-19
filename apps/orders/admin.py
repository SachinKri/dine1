from django.contrib import admin
from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "restaurant_id", "status", "total_amount", "created_at")
    list_filter = ("status",)
    search_fields = ("id", "user_id", "restaurant_id")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order_id", "menu_item_id", "quantity", "price")
