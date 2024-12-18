from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class AuthorDTO(BaseModel):
    id: Optional[UUID] = None
    firstname: str
    lastname: str
    description: Optional[str] = None
    resume: Optional[str] = None
