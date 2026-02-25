import os
from typing import List, Dict, Any
from domain.models import SearchQuery, SearchResultItem
from domain.base_classes import BaseSearchStrategy


class ImageSearchStrategy(BaseSearchStrategy):
    def __init__(self):
        super().__init__(name="image_search")

    def execute(self, query: SearchQuery, context: Dict[str, Any]) -> List[SearchResultItem]:
        em = context.get("embedding_manager")
        vdb = context.get("vector_db")
        if not em or not vdb:
            raise ValueError("Missing required dependencies in context")
        if not query.image_path:
            raise ValueError("Image path is required for image search")
        emb = em.get_image_embedding(query.image_path, "clip")
        filters = query.filters.to_dict() if query.filters else None
        results = vdb.search(emb, k=query.limit, filters=filters)
        self._log_search(query, len(results))
        return results

    def validate_query(self, query: SearchQuery) -> tuple[bool, str]:
        if not query.image_path:
            return False, "Image path is required"
        if not os.path.exists(query.image_path):
            return False, f"Image file not found: {query.image_path}"
        return True, "Valid"
