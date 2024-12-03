from fastapi import FastAPI

from .post_routes import post_router


def init_routes(app: FastAPI) -> None:
    app.include_router(post_router)
