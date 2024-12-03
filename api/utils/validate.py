from functools import wraps
from fastapi import Request


def requires_role(public: bool = False):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs.get("request")
            if request:
                request.state.public_route = public
            else:
                request.state.public_route = False

            return await func(*args, **kwargs)

        wrapper.public_route = public
        return wrapper

    return decorator
