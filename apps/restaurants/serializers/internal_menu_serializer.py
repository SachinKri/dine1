from rest_framework import serializers


class MenuItemRequestSerializer(serializers.Serializer):
    item_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)


class MenuValidationRequestSerializer(serializers.Serializer):
    restaurant_id = serializers.UUIDField()
    items = MenuItemRequestSerializer(many=True)

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("At least one menu item is required")
        return items
