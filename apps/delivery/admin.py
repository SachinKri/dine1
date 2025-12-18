from django.contrib import admin
from .models import Rider, DeliveryAssignment


@admin.register(Rider)
class RiderAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "is_available")
    list_filter = ("is_available",)
    search_fields = ("name", "phone")


@admin.register(DeliveryAssignment)
class DeliveryAssignmentAdmin(admin.ModelAdmin):
    list_display = ("id", "order_id", "rider_id", "status", "assigned_at")
    list_filter = ("status",)
    readonly_fields = ("assigned_at",)
