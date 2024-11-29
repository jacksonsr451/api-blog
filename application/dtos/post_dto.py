from typing import Optional

from pydantic import BaseModel

from .author_dto import AuthorDTO


class PostDTO(BaseModel):
    id: Optional[str] = None
    title: str
    description: Optional[str] = None
    body: Optional[str] = None
    slug: Optional[str] = None
    author: Optional[AuthorDTO] = None
    author_id: Optional[str] = None
    status: Optional[bool] = False
    thumbnail: Optional[str] = None
