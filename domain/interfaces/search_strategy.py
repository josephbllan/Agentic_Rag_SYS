from typing import Protocol, List, Dict, Any, runtime_checkable
from ..models import SearchQuery, SearchResultItem


@runtime_checkable
class ISearchStrategy(Protocol):
    @property
    def name(self) -> str: ...
    def execute(self, query: SearchQuery, context: Dict[str, Any]) -> List[SearchResultItem]: ...
    def validate_query(self, query: SearchQuery) -> tuple[bool, str]: ...
