from typing import Optional

from sqlalchemy.orm import Mapped
from sqlmodel import Field, Relationship

from application.interfaces.database_model import DatabaseModel


class PostModel(DatabaseModel, table=True):
    __tablename__ = 'posts'

    title: str
    description: Optional[str] = Field(default=None)
    body: Optional[str] = Field(default=None)
    slug: Optional[str] = Field(default=None)
    status: bool = Field(default=False)
    thumbnail: Optional[str] = Field(default=None)

    author_id: Optional[str] = Field(default=None, foreign_key='authors.id')
    author: Mapped[Optional['AuthorModel']] = Relationship(
        back_populates='posts'
    )


from infrastructure.models.author_model import AuthorModel
