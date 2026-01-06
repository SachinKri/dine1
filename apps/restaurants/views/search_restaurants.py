from rest_framework.generics import ListAPIView
from apps.restaurants.models import Restaurant
from apps.restaurants.serializers.restaurants import RestaurantSerializer
from apps.restaurants.cache.redis_client import redis_client
import json


# class RestaurantSearchView(ListAPIView):
#     serializer_class = RestaurantSerializer

#     def get_queryset(self):
#         q = self.request.query_params.get("q")

#         if not q:
#             return Restaurant.objects.none()

#         return Restaurant.objects.filter(
#             name__icontains=q,
#             is_active=True,
#             is_open=True
#         )

# After Redis Enabled    
class RestaurantSearchView(ListAPIView):
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        q = self.request.query_params.get("q")
        if not q:
            return Restaurant.objects.none()

        cache_key = f"restaurants:search:{q.lower()}"
        cached = redis_client.get(cache_key)

        if cached:
            return json.loads(cached)

        queryset = Restaurant.objects.filter(
            name__icontains=q,
            is_active=True,
            is_open=True
        )

        data = RestaurantSerializer(queryset, many=True).data
        redis_client.setex(cache_key, 300, json.dumps(data))

        return queryset