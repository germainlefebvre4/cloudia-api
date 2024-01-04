import redis

from app.core.config import settings


redis_c = redis.Redis(host=f"{settings.REDIS_SERVER}", port=f"{settings.REDIS_PORT}", decode_responses=True)
# redis_c = redis.Redis(host=f"{settings.REDIS_SERVER}", port=f"{settings.REDIS_PORT}", password=f"{settings.REDIS_PASSWORD}", decode_responses=True)
