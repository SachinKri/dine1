from rest_framework import serializers
from apps.restaurants.models import MenuCategory
from apps.restaurants.models import MenuItem

class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = "__all__"
        read_only_fields = ("id",)

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = "__all__"
        read_only_fields = ("id", "created_at")