from typing import Dict, Any
import logging
from .singleton_base import Singleton


class ConfigurationManager(Singleton):
    def __init__(self):
        """Initializes the configuration manager with an empty configuration store.
        Skips re-initialization if the singleton instance already exists.
        """
        if not hasattr(self, "_initialized"):
            self._config: Dict[str, Any] = {}
            self._logger = logging.getLogger(self.__class__.__name__)
            self._initialized = True

    def set(self, key: str, value: Any) -> None:
        """Stores a configuration value under the specified key."""
        self._config[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieves a configuration value by key, returning the default if not found."""
        return self._config.get(key, default)

    def update(self, config: Dict[str, Any]) -> None:
        """Merges a dictionary of configuration values into the current configuration."""
        self._config.update(config)

    def get_all(self) -> Dict[str, Any]:
        """Returns a shallow copy of the entire configuration dictionary."""
        return self._config.copy()

    def clear(self) -> None:
        """Clears all configuration entries from the store."""
        self._config.clear()

    def has(self, key: str) -> bool:
        """Checks whether a given key exists in the configuration."""
        return key in self._config

    def remove(self, key: str) -> None:
        """Removes a configuration entry by key, silently ignoring missing keys."""
        self._config.pop(key, None)
