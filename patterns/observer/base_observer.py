from abc import ABC, abstractmethod
from typing import Dict, Any


class Observer(ABC):
    @abstractmethod
    def update(self, subject: "Subject", event_type: str, data: Dict[str, Any]) -> None:
        """Handles a notification event from a subject.
        Subclasses must provide a concrete implementation for event processing.
        """
        pass
