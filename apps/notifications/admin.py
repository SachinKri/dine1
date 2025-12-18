from django.contrib import admin
from .models import NotificationLog


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "channel", "sent_at")
    list_filter = ("channel",)
    search_fields = ("user_id",)
    readonly_fields = ("sent_at",)
