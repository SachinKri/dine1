from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from apps.restaurants.models import Restaurant
from apps.restaurants.permissions import IsInternalService

class InternalRestaurantValidateView(APIView):
    permission_classes = [IsInternalService]

    def get(self, request, restaurant_id):
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            raise NotFound("Restaurant not found")

        if not restaurant.is_active:
            raise ValidationError("Restaurant is inactive")

        if not restaurant.is_open:
            raise ValidationError("Restaurant is closed")

        return Response({
            "restaurant_id": str(restaurant.id),
            "is_open": restaurant.is_open,
            "is_active": restaurant.is_active,
        })
