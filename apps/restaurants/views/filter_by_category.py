from rest_framework.generics import ListAPIView
from apps.restaurants.models import MenuItem
from apps.restaurants.serializers.menu import MenuItemSerializer


class MenuItemsByCategoryView(ListAPIView):
    """
    Customer-facing API to filter menu items by category
    """
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")

        return MenuItem.objects.filter(
            category_id=category_id,
            is_available=True
        )
