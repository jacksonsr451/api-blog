import re
from typing import Optional
from uuid import uuid4
from unidecode import unidecode

from .author_entity import AuthorEntity


class PostEntity:
    _id: str
    _title: str
    _description: Optional[str]
    _body: Optional[str]
    _slug: Optional[str]
    _author: Optional[AuthorEntity]
    _status: bool
    _thumbnail: Optional[str]

    def __init__(
        self,
        id: Optional[str] = None,
        title: str = "",
        status: bool = False,
        thumbnail: Optional[str] = None,
    ):
        if not title:
            raise ValueError('Title is required.')

        self._id = id if id else str(uuid4())
        self._title = title
        self._description = None
        self._body = None
        self._slug = None
        self._author = None
        self._status = status
        self._thumbnail = thumbnail

    def set_post_data(
        self,
        id: str,
        title: str,
        description: str,
        body: str,
        slug: str,
        author: AuthorEntity,
        status: bool,
        thumbnail: str,
    ) -> "PostEntity":
        if not title or not description or not body:
            raise ValueError('Title, description, and body are required.')

        self._id = id
        self._title = title
        self._description = description
        self._body = body
        self._slug = slug
        self._author = author
        self._status = status
        self._thumbnail = thumbnail
        return self

    def create_a_new_post(self, description: str, body: str) -> "PostEntity":
        if not description:
            raise ValueError('Description is required.')
        if not body:
            raise ValueError('Body is required.')

        self._description = description
        self._body = body
        self._slug = self.__generate_slug(self._title)
        return self

    def publish(self) -> "PostEntity":
        if not self._description or not self._body:
            raise ValueError(
                'Post must have a description and body before being published.'
            )
        self._status = True
        return self

    @property
    def id(self) -> str:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def body(self) -> Optional[str]:
        return self._body

    @property
    def slug(self) -> Optional[str]:
        return self._slug

    @property
    def author(self) -> Optional[AuthorEntity]:
        return self._author

    @property
    def status(self) -> bool:
        return self._status

    @property
    def thumbnail(self) -> Optional[str]:
        return self._thumbnail
    
    @thumbnail.setter
    def thumbnail(self, thumbnail) -> "PostEntity":
        self._thumbnail = thumbnail
        return self

    def __generate_slug(self, title: str) -> str:
        slug = unidecode(title)
        slug = re.sub(r"[^\w\s-]", "", slug)
        slug = re.sub(r"[\s-]+", "-", slug).strip("-")
        return slug.lower()

    def __repr__(self) -> str:
        return f"<PostEntity(id={self._id}, title={self._title}, status={'published' if self._status else 'draft'})>"
