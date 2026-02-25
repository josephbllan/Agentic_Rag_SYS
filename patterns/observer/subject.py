from typing import List, Dict, Any
import logging
from .base_observer import Observer


class Subject:
    def __init__(self):
        """Initializes the subject with an empty list of observers and a logger."""
        self._observers: List[Observer] = []
        self._logger = logging.getLogger(self.__class__.__name__)

    def attach(self, observer: Observer) -> None:
        """Attaches an observer to receive notifications from this subject.
        Prevents duplicate attachment of the same observer.
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """Detaches an observer so it no longer receives notifications from this subject."""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event_type: str, data: Dict[str, Any]) -> None:
        """Notifies all attached observers of an event, catching and logging any errors."""
        for observer in self._observers:
            try:
                observer.update(self, event_type, data)
            except Exception as e:
                self._logger.error(f"Error notifying {observer.__class__.__name__}: {e}")
