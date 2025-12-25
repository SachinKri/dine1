from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.users.permissions import IsRestaurantAdminRole
from apps.restaurants.models import MenuItem,MenuCategory,Restaurant
from apps.restaurants.serializers.bulk_menu import (
    BulkMenuUploadSerializer
)
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.db import transaction

class BulkMenuItemUploadView(APIView):
    """
    Bulk upload menu items using JSON
    """
    permission_classes = [IsAuthenticated, IsRestaurantAdminRole]

    def post(self, request):
        serializer = BulkMenuUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category_id = serializer.validated_data["category_id"]
        items = serializer.validated_data["items"]

        # 1️⃣ Validate category exists
        try:
            category = MenuCategory.objects.get(id=category_id, is_active=True)
        except MenuCategory.DoesNotExist:
            raise ValidationError("Invalid or inactive menu category.")

        # 2️⃣ Fetch restaurant of this category
        try:
            restaurant = Restaurant.objects.get(id=category.restaurant_id, is_active=True)
        except Restaurant.DoesNotExist:
            raise ValidationError("Associated restaurant does not exist or is inactive.")

        print("Restaurants ID",restaurant.owner_id)
        print("User ID",request.user.id)
        # 3️⃣ Validate restaurant ownership
        if int(restaurant.owner_id) != request.user.id:
            raise PermissionDenied(
                "You are not authorized to add items to this restaurant."
            )
        
        # # 2️⃣ Validate restaurant ownership
        # if category.restaurant_id != request.user.restaurant_id:
        #     raise PermissionDenied(
        #         "You are not authorized to add items to this category."
        #     )


        # 4️⃣ Prepare menu items (DO NOT SAVE YET)
        menu_items = []
        for item in items:
            menu_items.append(
                MenuItem(
                    category_id=category.id,
                    name=item["name"],
                    description=item.get("description", ""),
                    price=item["price"],
                    is_available=item.get("is_available", True),
                )
            )

        # created_items = []

        # for item in items:
        #     menu_item = MenuItem.objects.create(
        #         category_id=category_id,
        #         name=item["name"],
        #         description=item.get("description", ""),
        #         price=item["price"],
        #         is_available=item.get("is_available", True),
        #     )
        #     created_items.append(menu_item.id)

        # 5️⃣ Atomic + bulk insert
        with transaction.atomic():
            MenuItem.objects.bulk_create(menu_items)
        
        return Response(
            {
                "message": "Menu items uploaded successfully",
                "items_created": len(menu_items),
                "category_id": str(category.id),
                # "item_ids": menu_items.data,
            },
            status=status.HTTP_201_CREATED,
        )