from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsRestaurantAdminRole
from apps.restaurants.models import Restaurant
from apps.restaurants.serializers.restaurants import RestaurantSerializer
from rest_framework.exceptions import PermissionDenied


# CREATE
class RestaurantCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsRestaurantAdminRole]
    serializer_class = RestaurantSerializer

    def perform_create(self, serializer):
        serializer.save(owner_id=self.request.user.id)


# READ (List)
class RestaurantListView(generics.ListAPIView):
    queryset = Restaurant.objects.filter(is_active=True,is_open=True)
    serializer_class = RestaurantSerializer


# READ (Detail)
class RestaurantDetailView(generics.RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    lookup_field = "id"


# UPDATE
class RestaurantUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsRestaurantAdminRole]
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    lookup_field = "id"

'''
# DELETE
class RestaurantDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsRestaurantAdminRole]
    queryset = Restaurant.objects.all()
    lookup_field = "id"
'''

# DELETE
class RestaurantDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsRestaurantAdminRole]
    queryset = Restaurant.objects.all()
    lookup_field = "id"

    def perform_destroy(self, instance):
        """
        Ensure only the owner (restaurant admin) can delete the restaurant
        """
        if int(instance.owner_id) != self.request.user.id:
            raise PermissionDenied(
                "You are not authorized to delete this restaurant."
            )

        instance.delete()
