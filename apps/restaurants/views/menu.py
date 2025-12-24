from rest_framework.views import APIView
from rest_framework.response import Response
from apps.users.permissions import IsRestaurantAdminRole


class AddMenuItemView(APIView):
    permission_classes = [IsRestaurantAdminRole]

    def post(self, request):
        return Response({
            "message": "Menu item added successfully"
        })


from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsRestaurantAdminRole
from apps.restaurants.serializers.menu import MenuCategorySerializer


class MenuCategoryCreateView(APIView):
    permission_classes = [IsAuthenticated, IsRestaurantAdminRole]

    def post(self, request):
        serializer = MenuCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


from apps.restaurants.serializers.menu import MenuItemSerializer

class MenuItemCreateView(APIView):
    permission_classes = [IsAuthenticated, IsRestaurantAdminRole]

    def post(self, request):
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsRestaurantAdminRole
from apps.restaurants.models import MenuItem

class ToggleMenuItemAvailabilityView(APIView):
    permission_classes = [IsAuthenticated, IsRestaurantAdminRole]

    def patch(self, request, item_id):
        try:
            item = MenuItem.objects.get(id=item_id)
            item.is_available = not item.is_available
            item.save()
            return Response({"status": "updated"})
        except MenuItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)
