from abc import ABC, abstractmethod
from typing import Dict, Any
import logging


class BaseEventHandler(ABC):
    def __init__(self, event_type: str):
        """Initializes the handler for the specified event type.
        Sets up a logger scoped to the concrete subclass name.
        """
        self._event_type = event_type
        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def event_type(self) -> str:
        """Returns the event type this handler is responsible for."""
        return self._event_type

    @abstractmethod
    def handle(self, event_data: Dict[str, Any]) -> None:
        """Handles the incoming event data.
        Subclasses must implement the specific event processing logic.
        """
        pass

    def can_handle(self, event_type: str) -> bool:
        """Checks whether this handler supports the given event type."""
        return event_type == self._event_type

    def __repr__(self) -> str:
        """Returns a string representation including the event type."""
        return f"{self.__class__.__name__}(event_type='{self._event_type}')"
