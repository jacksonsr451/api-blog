from uuid import uuid4
from abc import ABC
from sqlmodel import SQLModel, Field, String


class DatabaseModel(SQLModel, ABC):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, sa_type=String)
