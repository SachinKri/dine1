from rest_framework.views import APIView
from rest_framework.response import Response
from apps.users.permissions import IsRestaurantAdminRole


class AddMenuItemView(APIView):
    permission_classes = [IsRestaurantAdminRole]

    def post(self, request):
        return Response({
            "message": "Menu item added successfully"
        })
