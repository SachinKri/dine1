from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.restaurants.serializers.internal_menu_serializer import (
    MenuValidationRequestSerializer
)
from apps.restaurants.services.menu_validation_service import (
    MenuValidationService
)


class InternalMenuValidationView(APIView):
    """
    Internal API for order service to validate menu items.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MenuValidationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_items = MenuValidationService.validate_and_fetch_items(
            restaurant_id=serializer.validated_data["restaurant_id"],
            items=serializer.validated_data["items"],
        )

        return Response({"items": validated_items})
