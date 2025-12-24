from rest_framework.generics import ListAPIView
from apps.restaurants.models import Restaurant
from apps.restaurants.serializers.restaurants import RestaurantSerializer


class RestaurantSearchView(ListAPIView):
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        q = self.request.query_params.get("q")

        if not q:
            return Restaurant.objects.none()

        return Restaurant.objects.filter(
            name__icontains=q,
            is_active=True,
            is_open=True
        )