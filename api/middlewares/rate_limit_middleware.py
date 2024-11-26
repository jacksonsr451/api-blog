import time

import redis
from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from api.database.redis import client_redis

r = client_redis


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path in ['/docs', '/openapi.json']:
            return await call_next(request)

        ip = request.client.host
        current_time = int(time.time())
        key = f'rate_limit:{ip}:{current_time // 60}'

        if r.get(key):
            raise HTTPException(status_code=429, detail='Too many requests')

        r.incr(key)
        r.expire(key, 60)

        response = await call_next(request)
        return response
