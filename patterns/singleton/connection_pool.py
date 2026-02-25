from typing import Dict, Any, Optional
import logging
from .singleton_base import Singleton


class ConnectionPoolManager(Singleton):
    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._pools: Dict[str, Any] = {}
            self._logger = logging.getLogger(self.__class__.__name__)
            self._initialized = True

    def register_pool(self, name: str, pool: Any) -> None:
        self._pools[name] = pool

    def get_pool(self, name: str) -> Optional[Any]:
        return self._pools.get(name)

    def close_pool(self, name: str) -> None:
        if name in self._pools:
            pool = self._pools[name]
            if hasattr(pool, "close"):
                pool.close()
            del self._pools[name]

    def close_all(self) -> None:
        for name in list(self._pools.keys()):
            self.close_pool(name)
