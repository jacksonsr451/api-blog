from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from api.setup_container import container

class DependencyInjectionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        dependencies = container.resolve_all(call_next)
        request.state.dependencies = dependencies
        response = await call_next(request)
        return response
