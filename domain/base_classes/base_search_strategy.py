from abc import ABC, abstractmethod
from typing import List, Dict, Any
import logging
from ..models import SearchQuery, SearchResultItem


class BaseSearchStrategy(ABC):
    def __init__(self, name: str):
        self._name = name
        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def execute(self, query: SearchQuery, context: Dict[str, Any]) -> List[SearchResultItem]:
        pass

    def validate_query(self, query: SearchQuery) -> tuple[bool, str]:
        if not query.query or not query.query.strip():
            return False, "Query is empty"
        return True, "Valid"

    def _log_search(self, query: SearchQuery, result_count: int) -> None:
        self._logger.info(
            f"Strategy '{self._name}' executed: query='{query.query[:50]}...', results={result_count}"
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self._name}')"
