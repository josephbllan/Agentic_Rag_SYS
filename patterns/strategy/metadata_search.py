import numpy as np
from typing import List, Dict, Any
from domain.models import SearchQuery, SearchResultItem
from domain.base_classes import BaseSearchStrategy


class MetadataSearchStrategy(BaseSearchStrategy):
    def __init__(self):
        """Initializes the metadata search strategy with its strategy name."""
        super().__init__(name="metadata_search")

    def execute(self, query: SearchQuery, context: Dict[str, Any]) -> List[SearchResultItem]:
        """Executes a metadata-based search using the provided filter criteria
        with a zero vector to retrieve filtered results from the database.
        """
        vector_db = context.get("vector_db")
        if not vector_db:
            raise ValueError("Missing required dependencies in context")
        if not query.filters:
            raise ValueError("Filters are required for metadata search")
        dummy = np.zeros(512, dtype=np.float32)
        results = vector_db.search(dummy, k=query.limit * 10, filters=query.filters.to_dict())
        final = results[: query.limit]
        self._log_search(query, len(final))
        return final

    def validate_query(self, query: SearchQuery) -> tuple[bool, str]:
        """Validates that the query contains filter criteria required for metadata search."""
        if not query.filters:
            return False, "Filters are required for metadata search"
        return True, "Valid"
