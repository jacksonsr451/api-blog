from typing import Optional
from uuid import UUID

from pydantic import BaseModel, HttpUrl

from .author_dto import AuthorDTO


class PostDTO(BaseModel):
    id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    body: Optional[str] = None
    slug: Optional[str] = None
    author: Optional[AuthorDTO] = None
    author_id: Optional[UUID] = None
    status: Optional[bool] = False
    thumbnail: Optional[HttpUrl] = None
