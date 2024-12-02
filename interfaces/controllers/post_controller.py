from api.config.settings import settings
from typing import List

from application.dtos.post_dto import PostDTO
from application.interfaces.post_service_interface import PostServiceIniterface
from interfaces.interfaces.post_controller_interface import PostControllerInterface

logger = settings.configure_logging()


class PostController(PostControllerInterface):
    def __init__(self, service: PostServiceIniterface):
        super().__init__(service)

    async def post(self, request: type[PostDTO], *args, **kargs) -> dict:
        try:
            self._service.create_a_new_post(request)
            await self._service.execute()
            logger.info("Succefule to create a new post!")
            return dict(message="Succefule to create a new post!", status=200)
        except Exception as error:
            logger.error(f"Error to create a post: {error}")
            return dict(detail="Error to create a new post!", status=400)

    async def put(self, id: str, request: type[PostDTO], *args, **kargs) -> dict:
        try:
            self._service.update_a_post(id)
            self._service.set_post_data(request)
            await self._service.execute()
            logger.info(f"Updated massege succefuly to post by id: {id}")
            return dict(
                message=f"Updated massege succefuly to post by id: {id}", status=200
            )
        except Exception as error:
            logger.error(f"Error to update a post: {error}")
            return dict(detail="Error to update a new post!", status=400)

    async def delete(self, id: str, *args, **kargs) -> dict:
        try:
            self._service.delete(id)
            await self._service.execute()
        except Exception as error:
            logger.error(f"Error to delete a post: {error}")
            return dict(detail="Error to delete a new post!", status=400)

    async def show(self, id: str, request: type[PostDTO], *args, **kargs) -> PostDTO:
        try:
            self._service.view(id)
            return dict(data=await self._service.execute(), status=200)
        except Exception as error:
            logger.error(f"Error to show a post with id: {id}, error: {error}")
            return dict(
                detail="Error to show a post with id: {id}, error: {error}", status=400
            )

    async def view(self, request: type[PostDTO], *args, **kargs) -> List[PostDTO]:
        try:
            self._service.list()
            return dict(data=await self._service.execute(), status=200)
        except Exception as error:
            logger.error(f"Error to list posts: {error}")
            return dict(detail="Error to list posts", status=400)
