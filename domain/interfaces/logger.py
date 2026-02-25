from typing import Protocol, Any, runtime_checkable


@runtime_checkable
class ILogger(Protocol):
    def debug(self, message: str, **kwargs: Any) -> None:
        """Logs a message at DEBUG level with optional keyword arguments."""
        ...

    def info(self, message: str, **kwargs: Any) -> None:
        """Logs a message at INFO level with optional keyword arguments."""
        ...

    def warning(self, message: str, **kwargs: Any) -> None:
        """Logs a message at WARNING level with optional keyword arguments."""
        ...

    def error(self, message: str, **kwargs: Any) -> None:
        """Logs a message at ERROR level with optional keyword arguments."""
        ...

    def critical(self, message: str, **kwargs: Any) -> None:
        """Logs a message at CRITICAL level with optional keyword arguments."""
        ...
