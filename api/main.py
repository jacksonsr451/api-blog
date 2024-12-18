from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from uvicorn import run

from .config.settings import settings
from .middlewares.jwt_middleware import JWTMiddleware
from .middlewares.rate_limit_middleware import RateLimitMiddleware
from .routes import init_routes

settings.configure_logging()

app = FastAPI(
    title='Api Blog',
    description='Api for management to a blog app with python and FastAPI',
    version='1.0.0',
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=['localhost', '*'])
app.add_middleware(RateLimitMiddleware)
app.add_middleware(JWTMiddleware)

init_routes(app=app)
