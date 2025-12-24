'''
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
'''

from django.contrib import admin
from .models import Restaurant, MenuCategory, MenuItem

# -----------------------------
# Restaurant Admin
# -----------------------------
@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "is_open",
        "is_active",
        "owner_id",
        "created_at",
    )

    list_filter = ("is_open", "is_active")
    search_fields = ("name", "address")
    ordering = ("name",)

    readonly_fields = ("id", "created_at")

    fieldsets = (
        ("Restaurant Information", {
            "fields": ("name", "description", "address")
        }),
        ("Ownership & Status", {
            "fields": ("owner_id", "is_open", "is_active")
        }),
        ("System Fields", {
            "fields": ("id", "created_at")
        }),
    )

# -----------------------------
# Menu Category Admin
# -----------------------------
@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "restaurant_id",
        "is_active",
    )

    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("name",)

    readonly_fields = ("id",)

    fieldsets = (
        ("Category Information", {
            "fields": ("name", "restaurant_id")
        }),
        ("Status", {
            "fields": ("is_active",)
        }),
        ("System Fields", {
            "fields": ("id",)
        }),
    )

# -----------------------------
# Menu Item Admin
# -----------------------------
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "category_id",
        "price",
        "is_available",
        "created_at",
    )

    list_filter = ("is_available",)
    search_fields = ("name",)
    ordering = ("name",)

    readonly_fields = ("id", "created_at")

    fieldsets = (
        ("Menu Item Details", {
            "fields": ("name", "description", "price")
        }),
        ("Category & Availability", {
            "fields": ("category_id", "is_available")
        }),
        ("System Fields", {
            "fields": ("id", "created_at")
        }),
    )