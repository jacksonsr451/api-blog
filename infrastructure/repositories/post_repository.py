from typing import List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlmodel import asc

from application.dtos.post_dto import PostDTO
from application.interfaces.base_repository_interface import (
    BaseRepositoryInterface,
)
from infrastructure.models.author_model import AuthorModel
from infrastructure.models.post_model import PostModel


class PostRepository(BaseRepositoryInterface):
    def __init__(self, session: AsyncSession, *args, **kargs):
        super().__init__(session, *args, **kargs)

    async def create(self, data: PostDTO) -> None:
        author_instance = AuthorModel(**data.author.model_dump())

        post_data = data.model_dump()
        post_data.pop('author', None)

        instance = PostModel(**post_data, author=author_instance)
        self._session.add(instance)

        try:
            await self._session.commit()
            await self._session.refresh(instance)
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e

    async def update(self, id, data: PostDTO) -> None:
        instance = await self._session.get(PostModel, id)

        if not instance:
            raise ValueError(f'Post com ID {id} não encontrado.')

        valid_keys = {column.name for column in PostModel.__table__.columns}
        for key, value in data.model_dump().items():
            if key in valid_keys:
                setattr(instance, key, value)

        try:
            await self._session.commit()
            await self._session.refresh(instance)
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e

    async def view(self, id) -> PostModel:
        instance = await self._session.get(PostModel, id)

        if not instance:
            raise ValueError(f'Post com ID {id} não encontrado.')

        return instance

    async def list(
        self, order_by: str = 'created_at'
    ) -> List[PostModel | None]:
        result = await self._session.execute(select(PostModel))

        return result.scalars().all()

    async def delete(self, id) -> None:
        instance = await self._session.get(PostModel, id)

        if not instance:
            raise ValueError(f'Post com ID {id} não encontrado.')

        try:
            await self._session.delete(instance)
            await self._session.commit()
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e
