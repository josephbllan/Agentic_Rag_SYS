from typing import Dict, Optional
import logging
from .singleton_base import Singleton


class LoggerManager(Singleton):
    def __init__(self):
        """Initializes the logger manager with default logging level and format settings.
        Skips re-initialization if the singleton instance already exists.
        """
        if not hasattr(self, "_initialized"):
            self._loggers: Dict[str, logging.Logger] = {}
            self._initialized = True
            self._default_level = logging.INFO
            self._default_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    def get_logger(self, name: str, level: Optional[int] = None, format_string: Optional[str] = None) -> logging.Logger:
        """Retrieves or creates a named logger with the specified level and format.
        Caches loggers to avoid duplicate handler registration.
        """
        if name not in self._loggers:
            lgr = logging.getLogger(name)
            lgr.setLevel(level or self._default_level)
            if not lgr.handlers:
                h = logging.StreamHandler()
                h.setFormatter(logging.Formatter(format_string or self._default_format))
                lgr.addHandler(h)
            self._loggers[name] = lgr
        return self._loggers[name]

    def set_default_level(self, level: int) -> None:
        """Updates the default logging level and applies it to all existing loggers."""
        self._default_level = level
        for lgr in self._loggers.values():
            lgr.setLevel(level)
