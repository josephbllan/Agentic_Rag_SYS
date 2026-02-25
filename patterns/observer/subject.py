from typing import List, Dict, Any
import logging
from .base_observer import Observer


class Subject:
    def __init__(self):
        self._observers: List[Observer] = []
        self._logger = logging.getLogger(self.__class__.__name__)

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event_type: str, data: Dict[str, Any]) -> None:
        for observer in self._observers:
            try:
                observer.update(self, event_type, data)
            except Exception as e:
                self._logger.error(f"Error notifying {observer.__class__.__name__}: {e}")
