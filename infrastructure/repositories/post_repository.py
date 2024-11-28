from typing import List

from application.interfaces.base_repository_interface import (
    BaseRepositoryInterface,
)
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.models.post_model import PostModel


class PostRepository(BaseRepositoryInterface):
    def __init__(self, session: AsyncSession, *args, **kargs):
        super().__init__(session, *args, **kargs)
        self.session = session

    async def create(self, data) -> None:
        return super().create(data)

    async def update(self, id, data) -> None:
        return super().update(id, data)

    async def view(self, id) -> PostModel:
        return super().view(id)

    async def list(self) -> List[PostModel | None]:
        return super().list()

    async def delete(self, id) -> None:
        return super().delete(id)
