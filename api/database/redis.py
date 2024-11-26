import redis

from api.config.settings import settings


def get_redis_client():
    return redis.StrictRedis.from_url(
        settings.REDIS_URL, decode_responses=True
    )


client_redis = get_redis_client()
