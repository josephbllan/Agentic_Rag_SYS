from typing import Protocol, List, runtime_checkable
from ..value_objects import QueryIntent


@runtime_checkable
class IQueryProcessor(Protocol):
    def process(self, query: str) -> QueryIntent:
        """Processes the raw query string and returns the interpreted query intent."""
        ...

    def validate(self, query: str) -> tuple[bool, str]:
        """Validates the query string and returns a tuple of (is_valid, message)."""
        ...

    def expand_query(self, query: str) -> List[str]:
        """Expands the query into a list of related or synonym queries."""
        ...
