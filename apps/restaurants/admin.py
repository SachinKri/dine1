from django.contrib import admin
from .models import Restaurant, MenuItem


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "city", "is_open", "rating")
    list_filter = ("city", "is_open")
    search_fields = ("name", "city")
    ordering = ("name",)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "restaurant_id", "price", "is_available")
    list_filter = ("is_available",)
    search_fields = ("name",)