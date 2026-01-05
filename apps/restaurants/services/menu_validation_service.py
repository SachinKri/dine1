from rest_framework.exceptions import ValidationError
from apps.restaurants.models import MenuItem, MenuCategory


class MenuValidationService:
    """
    Validates menu items against restaurant ownership
    and returns authoritative item data.
    """

    @staticmethod
    def validate_and_fetch_items(*, restaurant_id, items):
        # Map item_id → quantity
        item_quantity_map = {
            str(item["item_id"]): item["quantity"]
            for item in items
        }

        # Fetch menu items
        menu_items = (
            MenuItem.objects
            .filter(
                id__in=item_quantity_map.keys(),
                is_available=True,
            )
            .select_related(None)
        )

        if menu_items.count() != len(item_quantity_map):
            raise ValidationError(
                "One or more menu items are invalid or unavailable"
            )

        # Fetch categories for restaurant validation
        category_ids = {item.category_id for item in menu_items}

        valid_categories = set(
            MenuCategory.objects.filter(
                id__in=category_ids,
                restaurant_id=restaurant_id,
                is_active=True,
            ).values_list("id", flat=True)
        )

        if category_ids != valid_categories:
            raise ValidationError(
                "One or more items do not belong to this restaurant"
            )

        # Build validated response
        validated_items = []
        for item in menu_items:
            validated_items.append({
                "item_id": item.id,
                "name": item.name,
                "price": str(item.price),
                "quantity": item_quantity_map[str(item.id)],
            })

        return validated_items