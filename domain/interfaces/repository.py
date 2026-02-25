from typing import Protocol, Generic, List, Dict, Any, Optional, runtime_checkable
from ..types import T


@runtime_checkable
class IRepository(Protocol, Generic[T]):
    def add(self, entity: T) -> T:
        """Persists a new entity and returns the stored instance."""
        ...

    def get_by_id(self, id: Any) -> Optional[T]:
        """Retrieves an entity by its unique identifier, returning None if not found."""
        ...

    def update(self, entity: T) -> T:
        """Updates an existing entity and returns the updated instance."""
        ...

    def delete(self, id: Any) -> bool:
        """Deletes the entity with the given identifier and returns True if successful."""
        ...

    def find(self, criteria: Dict[str, Any]) -> List[T]:
        """Finds and returns all entities matching the given criteria dictionary."""
        ...

    def count(self) -> int:
        """Returns the total number of entities in the repository."""
        ...
