from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class Repository(ABC, Generic[T]):
    """
    Abstract base class for repositories.
    Provides basic CRUD operations.
    """

    @abstractmethod
    def get(self, id: str) -> T | None:
        """Retrieve an entity by its ID."""
        pass

    @abstractmethod
    def list(self) -> list[T]:
        """List all entities."""
        pass

    @abstractmethod
    def save(self, entity: T) -> T:
        """
        Save an entity.
        If it's new, create it.
        If it exists, update it, respecting optimistic locking.
        """
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        """Delete an entity by its ID."""
        pass
