from typing import List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import asc

from application.dtos.post_dto import PostDTO
from application.interfaces.base_repository_interface import (
    BaseRepositoryInterface,
)
from infrastructure.models.post_model import PostModel


class PostRepository(BaseRepositoryInterface):
    def __init__(self, session: AsyncSession, *args, **kargs):
        super().__init__(session, *args, **kargs)
        self._session = session

    async def create(self, data: PostDTO) -> None:
        instance = PostModel(**data.model_dump())
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

        for key, value in data.model_dump().items():
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
        query = self._session.query(PostModel)

        if order_by:
            query = query.order_by(asc(order_by))

        result = await self._session.execute(query)
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
