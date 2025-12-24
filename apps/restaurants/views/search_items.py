from rest_framework.generics import ListAPIView
from apps.restaurants.models import MenuItem
from apps.restaurants.serializers.menu import MenuItemSerializer


class FoodItemSearchView(ListAPIView):
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        q = self.request.query_params.get("q")

        if not q:
            return MenuItem.objects.none()

        return MenuItem.objects.filter(
            name__icontains=q,
            is_available=True
        )
