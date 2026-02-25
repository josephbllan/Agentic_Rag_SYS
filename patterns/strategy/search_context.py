from typing import List, Dict, Any, Optional
import logging
from domain.base_classes import BaseSearchStrategy
from domain.models import SearchQuery, SearchResultItem


class SearchContext:
    def __init__(self, strategy: Optional[BaseSearchStrategy] = None):
        """Initializes the search context with an optional search strategy."""
        self._strategy = strategy
        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def strategy(self) -> Optional[BaseSearchStrategy]:
        """Returns the currently configured search strategy, or None if not set."""
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: BaseSearchStrategy) -> None:
        """Sets a new search strategy and logs the strategy change."""
        self._logger.info(f"Switching strategy to: {strategy.name}")
        self._strategy = strategy

    def execute_search(self, query: SearchQuery, context: Dict[str, Any]) -> List[SearchResultItem]:
        """Delegates search execution to the currently configured strategy.
        Raises ValueError if no strategy has been set.
        """
        if self._strategy is None:
            raise ValueError("No search strategy set")
        return self._strategy.execute(query, context)

    def validate_query(self, query: SearchQuery) -> tuple[bool, str]:
        """Delegates query validation to the currently configured strategy.
        Raises ValueError if no strategy has been set.
        """
        if self._strategy is None:
            raise ValueError("No search strategy set")
        return self._strategy.validate_query(query)
