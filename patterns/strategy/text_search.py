from typing import List, Dict, Any
from domain.models import SearchQuery, SearchResultItem
from domain.base_classes import BaseSearchStrategy


class TextSearchStrategy(BaseSearchStrategy):
    def __init__(self):
        """Initializes the text search strategy with its strategy name."""
        super().__init__(name="text_search")

    def execute(self, query: SearchQuery, context: Dict[str, Any]) -> List[SearchResultItem]:
        """Executes a text-based search using CLIP text embeddings against the vector database."""
        em = context.get("embedding_manager")
        vdb = context.get("vector_db")
        if not em or not vdb:
            raise ValueError("Missing required dependencies in context")
        emb = em.get_text_embedding(query.query, "clip")
        filters = query.filters.to_dict() if query.filters else None
        results = vdb.search(emb, k=query.limit, filters=filters)
        self._log_search(query, len(results))
        return results

    def validate_query(self, query: SearchQuery) -> tuple[bool, str]:
        """Validates that the query contains a non-empty text within the 500-character limit."""
        if not query.query or not query.query.strip():
            return False, "Text query is empty"
        if len(query.query) > 500:
            return False, "Text query too long (max 500 characters)"
        return True, "Valid"
