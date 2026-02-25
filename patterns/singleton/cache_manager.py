from typing import Dict, Any, Optional
import logging
from .singleton_base import Singleton


class CacheManager(Singleton):
    def __init__(self):
        """Initializes the cache manager with empty cache and TTL stores.
        Skips re-initialization if the singleton instance already exists.
        """
        if not hasattr(self, "_initialized"):
            self._cache: Dict[str, Any] = {}
            self._ttl: Dict[str, float] = {}
            self._logger = logging.getLogger(self.__class__.__name__)
            self._initialized = True

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Stores a value in the cache with an optional time-to-live in seconds."""
        self._cache[key] = value
        if ttl is not None:
            import time
            self._ttl[key] = time.time() + ttl

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieves a value from the cache, returning the default if expired or missing."""
        if key in self._cache:
            if key in self._ttl:
                import time
                if time.time() > self._ttl[key]:
                    self.delete(key)
                    return default
            return self._cache[key]
        return default

    def delete(self, key: str) -> bool:
        """Removes a key and its TTL entry from the cache, returning whether it existed."""
        existed = key in self._cache
        self._cache.pop(key, None)
        self._ttl.pop(key, None)
        return existed

    def clear(self) -> None:
        """Clears all entries and TTL records from the cache."""
        self._cache.clear()
        self._ttl.clear()

    def exists(self, key: str) -> bool:
        """Checks whether a given key exists in the cache."""
        return key in self._cache

    def size(self) -> int:
        """Returns the total number of entries currently stored in the cache."""
        return len(self._cache)
