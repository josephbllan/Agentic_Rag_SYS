from typing import Dict, Any
import logging
from .base_observer import Observer
from .subject import Subject


class SearchEventObserver(Observer):
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._search_count = 0

    def update(self, subject: Subject, event_type: str, data: Dict[str, Any]) -> None:
        if event_type == "search_executed":
            self._search_count += 1
            self._logger.info(f"Search #{self._search_count}: query='{data.get('query', '')}', results={data.get('result_count', 0)}")
        elif event_type == "search_failed":
            self._logger.error(f"Search failed: {data.get('error', '')}")

    @property
    def search_count(self) -> int:
        return self._search_count
