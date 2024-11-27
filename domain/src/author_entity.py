from typing import Optional
from uuid import uuid4


class AuthorEntity:
    _id: str
    _firstname: str
    _lastname: str
    _description: Optional[str]
    _resume: Optional[str]

    def __init__(
        self,
        id: Optional[str] = None,
        firstname: str = "",
        lastname: str = "",
        description: Optional[str] = None,
        resume: Optional[str] = None,
    ):
        if not firstname:
            raise ValueError("Firstname is required.")
        if not lastname:
            raise ValueError("Lastname is required.")

        self._id = id if id else str(uuid4())
        self._firstname = firstname
        self._lastname = lastname
        self._description = description
        self._resume = resume

    def update_author_data(
        self,
        firstname: str,
        lastname: str,
        description: Optional[str] = None,
        resume: Optional[str] = None,
    ) -> "AuthorEntity":
        if not firstname:
            raise ValueError("Firstname is required.")
        if not lastname:
            raise ValueError("Lastname is required.")

        self._firstname = firstname
        self._lastname = lastname
        self._description = description
        self._resume = resume
        return self

    @property
    def id(self) -> str:
        return self._id

    @property
    def firstname(self) -> str:
        return self._firstname

    @property
    def lastname(self) -> str:
        return self._lastname

    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def resume(self) -> Optional[str]:
        return self._resume

    def __repr__(self) -> str:
        return f"<AuthorEntity(id={self._id}, name={self._firstname} {self._lastname})>"
