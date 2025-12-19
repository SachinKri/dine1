from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "order_id", "payment_mode", "status", "amount", "created_at")
    list_filter = ("payment_mode", "status")
    search_fields = ("order_id", "gateway_reference")
    readonly_fields = ("created_at",)
