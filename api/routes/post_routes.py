from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List
from uuid import UUID

from fastapi.security import HTTPBearer
from pydantic import BaseModel
from application.dtos.post_dto import PostDTO
from interfaces.controllers.post_controller import PostController
from api.setup_container import container
from api.utils.validate import requires_role
from api.config.settings import settings

logger = settings.configure_logging()

post_router = APIRouter(prefix="/api/v1/posts", tags=["Post Management"])

http_bearer = HTTPBearer()


class PostResponse(BaseModel):
    status: int
    message: str
    detail: str = None


def get_post_controller() -> PostController:
    service = container.resolve("PostServices")
    return PostController(service)


@post_router.post(
    "/",
    tags=["Post Management"],
    name="Create Post",
    summary="Create a new post",
    description="This endpoint allows the creation of a new post.",
    response_model=PostResponse,
    status_code=200,
    responses={
        200: {
            "description": "Post created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "status": 200,
                        "message": "Post created successfully",
                        "detail": "Post created successfully",
                    }
                }
            },
        },
        400: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {
                        "status": 400,
                        "message": "Error creating post",
                        "detail": "Invalid input data",
                    }
                }
            },
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {
                        "status": 500,
                        "message": "Internal Server Error",
                        "detail": "Error while creating post",
                    }
                }
            },
        },
    },
)
async def create_post(
    post: PostDTO,
    controller: PostController = Depends(get_post_controller),
    authorization: str = Depends(http_bearer),
):
    token = authorization.credentials
    try:
        response = await controller.post(request=post)
        if response["status"] != 200:
            raise HTTPException(status_code=400, detail=response["detail"])
        return response
    except Exception as error:
        logger.error(f"Error while creating post: {error}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@post_router.put(
    "/{post_id}",
    tags=["Post Management"],
    name="Update Post",
    summary="Update an existing post",
    description="This endpoint allows updating an existing post by its ID.",
    response_model=PostResponse,
    status_code=200,
    responses={
        200: {
            "description": "Post updated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "status": 200,
                        "message": "Post updated successfully",
                        "detail": "Post updated successfully",
                    }
                }
            },
        },
        400: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {
                        "status": 400,
                        "message": "Error updating post",
                        "detail": "Invalid input data",
                    }
                }
            },
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {
                        "status": 500,
                        "message": "Internal Server Error",
                        "detail": "Error while updating post",
                    }
                }
            },
        },
    },
)
async def update_post(
    post_id: UUID,
    post: PostDTO,
    controller: PostController = Depends(get_post_controller),
    authorization: str = Depends(http_bearer),
):
    token = authorization.credentials
    try:
        response = await controller.put(id=str(post_id), request=post)
        if response["status"] != 200:
            raise HTTPException(status_code=400, detail=response["detail"])
        return response
    except Exception as error:
        logger.error(f"Error while updating post {post_id}: {error}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@post_router.delete(
    "/{post_id}",
    tags=["Post Management"],
    name="Delete Post",
    summary="Delete an existing post",
    description="This endpoint allows deleting an existing post by its ID.",
    response_model=PostResponse,
    status_code=200,
    responses={
        200: {
            "description": "Post deleted successfully",
            "content": {
                "application/json": {
                    "example": {
                        "status": 200,
                        "message": "Post deleted successfully",
                        "detail": "Post deleted successfully",
                    }
                }
            },
        },
        400: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {
                        "status": 400,
                        "message": "Error deleting post",
                        "detail": "Invalid post ID",
                    }
                }
            },
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {
                        "status": 500,
                        "message": "Internal Server Error",
                        "detail": "Error while deleting post",
                    }
                }
            },
        },
    },
)
async def delete_post(
    post_id: UUID,
    controller: PostController = Depends(get_post_controller),
    authorization: str = Depends(http_bearer),
):
    token = authorization.credentials
    try:
        response = await controller.delete(id=str(post_id))
        if response["status"] != 200:
            raise HTTPException(status_code=400, detail=response["detail"])
        return response
    except Exception as error:
        logger.error(f"Error while deleting post {post_id}: {error}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@post_router.get(
    "/{post_id}",
    tags=["Post Management"],
    name="Show Post",
    summary="Get a post by ID",
    description="This endpoint allows retrieving a post by its ID.",
    response_model=dict,
    status_code=200,
    responses={
        200: {
            "description": "Post retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "status": 200,
                        "message": "Post found",
                        "detail": {
                            "post_id": "<post_id>",
                            "title": "<title>",
                            "content": "<content>",
                        },
                    }
                }
            },
        },
        400: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {
                        "status": 400,
                        "message": "Error retrieving post",
                        "detail": "Post not found",
                    }
                }
            },
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {
                        "status": 500,
                        "message": "Internal Server Error",
                        "detail": "Error while retrieving post",
                    }
                }
            },
        },
    },
)
async def show_post(
    post_id: UUID,
    controller: PostController = Depends(get_post_controller),
    authorization: str = Depends(http_bearer),
):
    token = authorization.credentials
    try:
        response = await controller.show(id=str(post_id), request=None)
        if response["status"] != 200:
            raise HTTPException(status_code=400, detail=response["detail"])
        return response
    except Exception as error:
        logger.error(f"Error while retrieving post {post_id}: {error}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@post_router.get(
    "/",
    tags=["Post Management"],
    name="List Posts",
    summary="List all posts",
    description="This endpoint allows listing all posts.",
    response_model=List[dict],
    status_code=200,
    responses={
        200: {
            "description": "Posts listed successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "post_id": "<post_id>",
                            "title": "<title>",
                            "content": "<content>",
                        }
                    ]
                }
            },
        },
        400: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {
                        "status": 400,
                        "message": "Error listing posts",
                        "detail": "Invalid input data",
                    }
                }
            },
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {
                        "status": 500,
                        "message": "Internal Server Error",
                        "detail": "Error while listing posts",
                    }
                }
            },
        },
    },
)
@requires_role(public=True)
async def list_posts(
    request: Request,
    controller: PostController = Depends(get_post_controller),
):
    try:
        response = await controller.view(request=None)
        if response["status"] != 200:
            raise HTTPException(status_code=400, detail=response["detail"])
        return response or []
    except Exception as error:
        logger.error(f"Error while listing posts: {error}")
        return []
