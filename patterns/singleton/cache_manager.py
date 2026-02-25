from typing import Dict, Any, Optional
import logging
from .singleton_base import Singleton


class CacheManager(Singleton):
    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._cache: Dict[str, Any] = {}
            self._ttl: Dict[str, float] = {}
            self._logger = logging.getLogger(self.__class__.__name__)
            self._initialized = True

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        self._cache[key] = value
        if ttl is not None:
            import time
            self._ttl[key] = time.time() + ttl

    def get(self, key: str, default: Any = None) -> Any:
        if key in self._cache:
            if key in self._ttl:
                import time
                if time.time() > self._ttl[key]:
                    self.delete(key)
                    return default
            return self._cache[key]
        return default

    def delete(self, key: str) -> bool:
        existed = key in self._cache
        self._cache.pop(key, None)
        self._ttl.pop(key, None)
        return existed

    def clear(self) -> None:
        self._cache.clear()
        self._ttl.clear()

    def exists(self, key: str) -> bool:
        return key in self._cache

    def size(self) -> int:
        return len(self._cache)
