from typing import List, Optional

from sqlalchemy.orm import Mapped
from sqlmodel import Field, Relationship

from application.interfaces.database_model import DatabaseModel


class AuthorModel(DatabaseModel, table=True):
    __tablename__ = 'authors'

    firstname: str
    lastname: str
    description: Optional[str] = Field(default=None)
    resume: Optional[str] = Field(default=None)

    posts: Mapped[List['PostModel']] = Relationship(back_populates='author')


from infrastructure.models.post_model import PostModel
