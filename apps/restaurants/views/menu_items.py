from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsRestaurantAdminRole
from apps.restaurants.models import MenuItem
from apps.restaurants.serializers.menu import MenuItemSerializer


class MenuItemCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsRestaurantAdminRole]
    serializer_class = MenuItemSerializer


class MenuItemListView(generics.ListAPIView):
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        return MenuItem.objects.filter(
            category_id=self.request.query_params.get("category_id"),
            is_available=True
        )


class MenuItemUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsRestaurantAdminRole]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    lookup_field = "id"


class MenuItemDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsRestaurantAdminRole]
    queryset = MenuItem.objects.all()
    lookup_field = "id"