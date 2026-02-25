import numpy as np
from typing import List, Dict, Any
from domain.models import SearchQuery, SearchResultItem
from domain.base_classes import BaseSearchStrategy


class MetadataSearchStrategy(BaseSearchStrategy):
    def __init__(self):
        super().__init__(name="metadata_search")

    def execute(self, query: SearchQuery, context: Dict[str, Any]) -> List[SearchResultItem]:
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
        if not query.filters:
            return False, "Filters are required for metadata search"
        return True, "Valid"
