from abc import ABC, abstractmethod
from typing import List, Optional

from pydantic import BaseModel

from .database_model import DatabaseModel


class BaseRepositoryInterface(ABC):
    def __init__(self, model: DatabaseModel, *args, **kargs):
        super().__init__(model, *args, **kargs)

    @abstractmethod
    def create(self, data: DatabaseModel) -> None:
        """Create a new entry."""
        pass

    @abstractmethod
    def view(self, id: str) -> Optional[DatabaseModel]:
        """View an entry by its ID."""
        pass

    @abstractmethod
    def list(self) -> List[DatabaseModel]:
        """List all entries."""
        pass

    @abstractmethod
    def update(self, id: str, data: DatabaseModel) -> None:
        """Update an entry by its ID."""
        pass

    @abstractmethod
    def delete(self, id: str) -> None:
        """Delete an entry by its ID."""
        pass
