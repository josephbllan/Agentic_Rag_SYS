from abc import ABC, abstractmethod
from typing import List, Dict, Any
import logging
from ..models import SearchQuery, SearchResultItem


class BaseSearchStrategy(ABC):
    def __init__(self, name: str):
        """Initializes the search strategy with the given name.
        Sets up a logger scoped to the concrete subclass.
        """
        self._name = name
        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def name(self) -> str:
        """Returns the name identifying this search strategy."""
        return self._name

    @abstractmethod
    def execute(self, query: SearchQuery, context: Dict[str, Any]) -> List[SearchResultItem]:
        """Executes the search strategy against the given query and context.
        Subclasses must implement the specific search algorithm.
        """
        pass

    def validate_query(self, query: SearchQuery) -> tuple[bool, str]:
        """Validates the search query and returns a tuple of (is_valid, message).
        Rejects empty or whitespace-only query strings.
        """
        if not query.query or not query.query.strip():
            return False, "Query is empty"
        return True, "Valid"

    def _log_search(self, query: SearchQuery, result_count: int) -> None:
        """Logs the strategy execution details including query text and result count."""
        self._logger.info(
            f"Strategy '{self._name}' executed: query='{query.query[:50]}...', results={result_count}"
        )

    def __repr__(self) -> str:
        """Returns a string representation including the strategy name."""
        return f"{self.__class__.__name__}(name='{self._name}')"
