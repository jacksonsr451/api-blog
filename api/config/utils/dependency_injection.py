import functools
from typing import Callable

from api.config.settings import settings


def dependency_injection(fn: Callable):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        settings.CONTAINER.resolve_all(fn)
        return fn(*args, **kwargs)

    return wrapper
