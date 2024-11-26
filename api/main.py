from uvicorn import run

from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from .config.settings import settings
from .routes import init_routes

from .middlewares.jwt_middleware import JWTMiddleware
from .middlewares.rate_limit_middleware import RateLimitMiddleware

settings.configure_logging()

app = FastAPI(title='Api Blog', description="Api for management to a blog app with python and FastAPI", version='1.0.0')

app.add_middleware(TrustedHostMiddleware, allowed_hosts=['localhost', '*'])
app.add_middleware(RateLimitMiddleware)
app.add_middleware(JWTMiddleware)

init_routes(app=app)


def create_app() -> None:
    run("api.main:app", host=settings.SERVER_HOST, port=settings.SERVER_PORT, reload=settings.SERVER_RELOAD)
