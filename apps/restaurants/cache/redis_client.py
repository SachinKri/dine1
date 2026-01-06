import redis
from django.conf import settings

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    socket_timeout=settings.REDIS_SOCKET_TIMEOUT,
    retry_on_timeout=settings.REDIS_RETRY_ON_TIMEOUT,
    decode_responses=True
)