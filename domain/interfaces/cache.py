from typing import Protocol, Any, Optional, runtime_checkable


@runtime_checkable
class ICache(Protocol):
    def get(self, key: str) -> Optional[Any]:
        """Retrieves a cached value by its key, returning None if not found."""
        ...

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Stores a value in the cache under the given key with an optional TTL in seconds."""
        ...

    def delete(self, key: str) -> bool:
        """Removes the entry for the given key and returns True if it existed."""
        ...

    def clear(self) -> None:
        """Clears all entries from the cache."""
        ...

    def exists(self, key: str) -> bool:
        """Checks whether a value exists in the cache for the given key."""
        ...
