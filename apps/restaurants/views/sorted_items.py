from rest_framework.generics import ListAPIView
from apps.restaurants.models import MenuItem
from apps.restaurants.serializers.menu import MenuItemSerializer
from apps.restaurants.pagination import FoodItemPagination

class MenuItemListView(ListAPIView):
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        return MenuItem.objects.filter(
            category_id=self.request.query_params.get("category_id"),
            is_available=True
        )

class SortedMenuItemsView(ListAPIView):
    """
    Customer-facing API to:
    - Filter by category
    - Sort by price
    - Paginate results
    """
    serializer_class = MenuItemSerializer
    pagination_class = FoodItemPagination

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        sort = self.request.query_params.get("sort")

        queryset = MenuItem.objects.filter(
            category_id=category_id,
            is_available=True
        )

        if sort == "price_asc":
            queryset = queryset.order_by("price")
        elif sort == "price_desc":
            queryset = queryset.order_by("-price")

        return queryset
