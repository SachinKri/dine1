from rest_framework.views import APIView
from rest_framework.response import Response
from apps.restaurants.models import Restaurant
from apps.restaurants.serializers.restaurants import RestaurantSerializer


class RestaurantListView(APIView):
    """
    List all active restaurants
    """
    def get(self, request):
        qs = Restaurant.objects.filter(is_active=True, is_open=True)
        serializer = RestaurantSerializer(qs, many=True)
        return Response(serializer.data)
    

from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsRestaurantAdminRole


class RestaurantCreateView(APIView):
    permission_classes = [IsAuthenticated, IsRestaurantAdminRole]

    def post(self, request):
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner_id=request.user.id)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)