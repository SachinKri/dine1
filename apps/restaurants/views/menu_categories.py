from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsRestaurantAdminRole
from apps.restaurants.models import MenuCategory
from apps.restaurants.serializers.menu import MenuCategorySerializer


class MenuCategoryCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsRestaurantAdminRole]
    serializer_class = MenuCategorySerializer


class MenuCategoryListView(generics.ListAPIView):
    serializer_class = MenuCategorySerializer

    def get_queryset(self):
        return MenuCategory.objects.filter(
            restaurant_id=self.request.query_params.get("restaurant_id"),
            is_active=True
        )


class MenuCategoryUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsRestaurantAdminRole]
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer
    lookup_field = "id"


class MenuCategoryDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsRestaurantAdminRole]
    queryset = MenuCategory.objects.all()
    lookup_field = "id"
