from rest_framework import serializers
from apps.restaurants.models import MenuItem

class BulkMenuItemSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    is_available = serializers.BooleanField(default=True)


class BulkMenuUploadSerializer(serializers.Serializer):
    category_id = serializers.UUIDField()
    items = BulkMenuItemSerializer(many=True)