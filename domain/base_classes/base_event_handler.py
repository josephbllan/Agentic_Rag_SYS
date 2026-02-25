from abc import ABC, abstractmethod
from typing import Dict, Any
import logging


class BaseEventHandler(ABC):
    def __init__(self, event_type: str):
        self._event_type = event_type
        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def event_type(self) -> str:
        return self._event_type

    @abstractmethod
    def handle(self, event_data: Dict[str, Any]) -> None:
        pass

    def can_handle(self, event_type: str) -> bool:
        return event_type == self._event_type

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(event_type='{self._event_type}')"
