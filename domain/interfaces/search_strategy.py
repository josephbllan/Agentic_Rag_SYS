from typing import Protocol, List, Dict, Any, runtime_checkable
from ..models import SearchQuery, SearchResultItem


@runtime_checkable
class ISearchStrategy(Protocol):
    @property
    def name(self) -> str:
        """Returns the name identifying this search strategy."""
        ...

    def execute(self, query: SearchQuery, context: Dict[str, Any]) -> List[SearchResultItem]:
        """Executes the search strategy for the given query and context."""
        ...

    def validate_query(self, query: SearchQuery) -> tuple[bool, str]:
        """Validates the search query and returns a tuple of (is_valid, message)."""
        ...
