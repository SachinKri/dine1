from rest_framework.exceptions import Throttled
from apps.restaurants.cache.redis_client import redis_client

MAX_TOKENS = 3          # 3 restaurants
WINDOW_SECONDS = 3600   # per hour

def enforce_restaurant_create_rate_limit(user_id):
    """
    Token bucket implementation using Redis.
    Allows MAX_TOKENS creations per WINDOW_SECONDS.
    """

    key = f"rate_limit:restaurant:create:{user_id}"

    current = redis_client.get(key)

    if current is None:
        # First request: initialize bucket
        redis_client.setex(key, WINDOW_SECONDS, 1)
        return

    if int(current) >= MAX_TOKENS:
        raise Throttled(
            detail="Restaurant creation limit exceeded. Try again later."
        )

    redis_client.incr(key)