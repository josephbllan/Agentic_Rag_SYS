from abc import ABC, abstractmethod
from typing import Generic, List, Dict, Any, Optional
import logging
from ..types import T


class BaseRepository(ABC, Generic[T]):
    def __init__(self, entity_type: type):
        """Initializes the repository for the given entity type.
        Sets up a logger scoped to the concrete subclass name.
        """
        self._entity_type = entity_type
        self._logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def add(self, entity: T) -> T:
        """Persists a new entity and returns the stored instance.
        Subclasses must implement the storage-specific insertion logic.
        """
        pass

    @abstractmethod
    def get_by_id(self, id: Any) -> Optional[T]:
        """Retrieves an entity by its unique identifier.
        Returns None if no entity with the given id exists.
        """
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        """Updates an existing entity and returns the updated instance.
        Subclasses must implement the storage-specific update logic.
        """
        pass

    @abstractmethod
    def delete(self, id: Any) -> bool:
        """Deletes the entity with the given identifier.
        Returns True if the entity was successfully removed, False otherwise.
        """
        pass

    @abstractmethod
    def find(self, criteria: Dict[str, Any]) -> List[T]:
        """Finds and returns all entities matching the given criteria dictionary.
        Subclasses must implement the storage-specific query logic.
        """
        pass

    def count(self) -> int:
        """Returns the total number of entities in the repository."""
        return len(self.find({}))

    def exists(self, id: Any) -> bool:
        """Checks whether an entity with the given identifier exists."""
        return self.get_by_id(id) is not None

    def __repr__(self) -> str:
        """Returns a string representation including the entity type name."""
        return f"{self.__class__.__name__}(entity_type={self._entity_type.__name__})"
