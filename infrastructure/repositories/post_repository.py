from typing import List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

from application.dtos.post_dto import PostDTO
from application.interfaces.base_repository_interface import (
    BaseRepositoryInterface,
)
from application.interfaces.post_repository_interface import PostRepositoryInterface
from infrastructure.models.author_model import AuthorModel
from infrastructure.models.post_model import PostModel


class PostRepository(PostRepositoryInterface):
    def __init__(self, session, model, *args, **kargs):
        super().__init__(session, model, *args, **kargs)

    async def create(self, data: PostDTO) -> None:
        author_instance = AuthorModel(**data.author.model_dump())

        post_data = data.model_dump()
        post_data.pop("author", None)

        instance = PostModel(**post_data, author=author_instance)
        self._session.add(instance)

        try:
            await self._session.commit()
            await self._session.refresh(instance)
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e
