from typing import Dict, Any
import logging
from .base_observer import Observer
from .subject import Subject


class IndexingEventObserver(Observer):
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._indexed_count = 0
        self._failed_count = 0

    def update(self, subject: Subject, event_type: str, data: Dict[str, Any]) -> None:
        if event_type == "image_indexed":
            self._indexed_count += 1
            if self._indexed_count % 100 == 0:
                self._logger.info(f"Indexed {self._indexed_count} images")
        elif event_type == "indexing_failed":
            self._failed_count += 1
            self._logger.warning(f"Indexing failed: {data.get('filename', '')}: {data.get('error', '')}")
        elif event_type == "indexing_complete":
            self._logger.info(f"Complete: {data.get('successful', 0)}/{data.get('total', 0)} ok")

    @property
    def stats(self) -> Dict[str, int]:
        return {"indexed": self._indexed_count, "failed": self._failed_count}
