from typing import List, Dict, Any, Optional
import logging
from domain.base_classes import BaseSearchStrategy
from domain.models import SearchQuery, SearchResultItem


class SearchContext:
    def __init__(self, strategy: Optional[BaseSearchStrategy] = None):
        self._strategy = strategy
        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def strategy(self) -> Optional[BaseSearchStrategy]:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: BaseSearchStrategy) -> None:
        self._logger.info(f"Switching strategy to: {strategy.name}")
        self._strategy = strategy

    def execute_search(self, query: SearchQuery, context: Dict[str, Any]) -> List[SearchResultItem]:
        if self._strategy is None:
            raise ValueError("No search strategy set")
        return self._strategy.execute(query, context)

    def validate_query(self, query: SearchQuery) -> tuple[bool, str]:
        if self._strategy is None:
            raise ValueError("No search strategy set")
        return self._strategy.validate_query(query)
