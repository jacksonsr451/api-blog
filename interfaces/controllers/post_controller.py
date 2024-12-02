from typing import List
from fastapi import Request

from application.dtos.post_dto import PostDTO
from application.interfaces.post_service_interface import PostServiceIniterface
from interfaces.interfaces.post_controller_interface import PostControllerInterface


class PostController(PostControllerInterface):
    def __init__(self, service: PostServiceIniterface):
        super().__init__(service)

    async def post(self, request: type[Request], *args, **kargs) -> str:
        pass

    async def put(self, request: type[Request], *args, **kargs) -> str:
        pass

    async def delete(self, request: type[Request], *args, **kargs) -> str:
        pass

    async def show(self, request: type[Request], *args, **kargs) -> PostDTO:
        pass

    async def view(self, request: type[Request], *args, **kargs) -> List[PostDTO]:
        pass
