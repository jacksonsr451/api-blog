from abc import ABC, abstractmethod
from typing import List, Optional

from pydantic import BaseModel as BaseDTO

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

from .database_model import DatabaseModel


class BaseRepositoryInterface(ABC):
    def __init__(self, session: type[AsyncSession], model: type[DatabaseModel], *args, **kargs):
        self._session = session
        self._model: type[DatabaseModel] = model

    async def create(self, data: BaseDTO) -> None:
        instance = self._model(**data.model_dump())
        self._session.add(instance)

        try:
            await self._session.commit()
            await self._session.refresh(instance)
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e

    async def update(self, id, data: BaseDTO) -> None:
        instance = await self._session.get(self._model, id)

        if not instance:
            raise ValueError(f'Post com ID {id} não encontrado.')

        valid_keys = {column.name for column in self._model.__table__.columns}
        for key, value in data.model_dump().items():
            if key in valid_keys:
                setattr(instance, key, value)

        try:
            await self._session.commit()
            await self._session.refresh(instance)
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e

    async def view(self, id) -> Optional[DatabaseModel]:
        instance = await self._session.get(self._model, id)

        if not instance:
            raise ValueError(f'Post com ID {id} não encontrado.')

        return instance

    async def list(
        self, order_by: str = 'created_at'
    ) -> List[Optional[DatabaseModel] | None]:
        result = await self._session.execute(select(self._model))

        return result.scalars().all()

    async def delete(self, id) -> None:
        instance = await self._session.get(self._model, id)

        if not instance:
            raise ValueError(f'Post com ID {id} não encontrado.')

        try:
            await self._session.delete(instance)
            await self._session.commit()
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e
