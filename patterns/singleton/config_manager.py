from typing import Dict, Any
import logging
from .singleton_base import Singleton


class ConfigurationManager(Singleton):
    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._config: Dict[str, Any] = {}
            self._logger = logging.getLogger(self.__class__.__name__)
            self._initialized = True

    def set(self, key: str, value: Any) -> None:
        self._config[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)

    def update(self, config: Dict[str, Any]) -> None:
        self._config.update(config)

    def get_all(self) -> Dict[str, Any]:
        return self._config.copy()

    def clear(self) -> None:
        self._config.clear()

    def has(self, key: str) -> bool:
        return key in self._config

    def remove(self, key: str) -> None:
        self._config.pop(key, None)
