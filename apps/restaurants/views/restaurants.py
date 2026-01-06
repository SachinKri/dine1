from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsRestaurantAdminRole
from apps.restaurants.models import Restaurant
from apps.restaurants.serializers.restaurants import RestaurantSerializer
from rest_framework.exceptions import PermissionDenied

from apps.restaurants.cache.redis_client import redis_client
import json


# CREATE
# class RestaurantCreateView(generics.CreateAPIView):
#     permission_classes = [IsAuthenticated, IsRestaurantAdminRole]
#     serializer_class = RestaurantSerializer

#     def perform_create(self, serializer):
#         serializer.save(owner_id=self.request.user.id)

# CREATE
# After Redis Enabled
class RestaurantCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsRestaurantAdminRole]
    serializer_class = RestaurantSerializer

    def perform_create(self, serializer):
        restaurant = serializer.save(owner_id=self.request.user.id)

        # Write-through cache update
        redis_client.hset(
            f"restaurant:status:{restaurant.id}",
            mapping={
                "is_open": int(restaurant.is_open),
                "is_active": int(restaurant.is_active)
            }
        )

        # Invalidate list cache
        redis_client.delete("restaurants:list:active_open")

# READ (List)
# class RestaurantListView(generics.ListAPIView):
#     queryset = Restaurant.objects.filter(is_active=True,is_open=True)
#     serializer_class = RestaurantSerializer

# After Redis Enabled
class RestaurantListView(generics.ListAPIView):
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        cache_key = "restaurants:list:active_open"

        try:
            cached_data = redis_client.get(cache_key)
            if cached_data:
                return json.loads(cached_data)
        except Exception:
            pass  # Fail gracefully

        queryset = Restaurant.objects.filter(
            is_active=True,
            is_open=True
        )

        serialized_data = RestaurantSerializer(queryset, many=True).data
        redis_client.setex(cache_key, 600, json.dumps(serialized_data))

        return queryset

# READ (Detail)
# class RestaurantDetailView(generics.RetrieveAPIView):
#     queryset = Restaurant.objects.all()
#     serializer_class = RestaurantSerializer
#     lookup_field = "id"

# After Redis Enabled
class RestaurantDetailView(generics.RetrieveAPIView):
    serializer_class = RestaurantSerializer
    lookup_field = "id"

    def get_object(self):
        restaurant_id = self.kwargs["id"]
        cache_key = f"restaurant:detail:{restaurant_id}"

        cached = redis_client.get(cache_key)
        if cached:
            return json.loads(cached)

        obj = Restaurant.objects.get(id=restaurant_id)
        redis_client.setex(
            cache_key,
            1800,
            json.dumps(RestaurantSerializer(obj).data)
        )
        return obj


# UPDATE
# class RestaurantUpdateView(generics.UpdateAPIView):
#     permission_classes = [IsAuthenticated, IsRestaurantAdminRole]
#     queryset = Restaurant.objects.all()
#     serializer_class = RestaurantSerializer
#     lookup_field = "id"


# UPDATE
# After Redis Enabled
class RestaurantUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsRestaurantAdminRole]
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    lookup_field = "id"

    def perform_update(self, serializer):
        restaurant = self.get_object()

        # Ensure only creator can update
        if restaurant.owner_id != self.request.user.id:
            raise PermissionDenied(
                "You are not authorized to update this restaurant."
            )

        updated_restaurant = serializer.save()

        # Write-through cache update (status cache)
        redis_client.hset(
            f"restaurant:status:{updated_restaurant.id}",
            mapping={
                "is_open": int(updated_restaurant.is_open),
                "is_active": int(updated_restaurant.is_active),
            }
        )

        # Invalidate dependent caches
        redis_client.delete(f"restaurant:detail:{updated_restaurant.id}")
        redis_client.delete("restaurants:list:active_open")


'''
# DELETE
class RestaurantDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsRestaurantAdminRole]
    queryset = Restaurant.objects.all()
    lookup_field = "id"
'''

# DELETE
# class RestaurantDeleteView(generics.DestroyAPIView):
#     permission_classes = [IsAuthenticated, IsRestaurantAdminRole]
#     queryset = Restaurant.objects.all()
#     lookup_field = "id"

#     def perform_destroy(self, instance):
#         """
#         Ensure only the owner (restaurant admin) can delete the restaurant
#         """
#         # if int(instance.owner_id) != self.request.user.id:
#         if instance.owner_id != self.request.user.id:
#             raise PermissionDenied(
#                 "You are not authorized to delete this restaurant."
#             )

#         instance.delete()

# DELETE
# After Redis Enabled
class RestaurantDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsRestaurantAdminRole]
    queryset = Restaurant.objects.all()
    lookup_field = "id"

    def perform_destroy(self, instance):
        """
        Ensure only the owner (restaurant admin) can delete the restaurant
        """
        if instance.owner_id != self.request.user.id:
            raise PermissionDenied(
                "You are not authorized to delete this restaurant."
            )

        restaurant_id = instance.id

        # Delete from database
        instance.delete()

        # Write-through cache cleanup
        redis_client.delete(f"restaurant:status:{restaurant_id}")
        redis_client.delete(f"restaurant:detail:{restaurant_id}")
        redis_client.delete("restaurants:list:active_open")
