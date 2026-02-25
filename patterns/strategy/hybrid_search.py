import os
from typing import List, Dict, Any, Optional
from domain.models import SearchQuery, SearchResultItem
from domain.base_classes import BaseSearchStrategy


class HybridSearchStrategy(BaseSearchStrategy):
    def __init__(self, weights: Optional[Dict[str, float]] = None):
        super().__init__(name="hybrid_search")
        self._weights = weights or {"visual": 0.4, "text": 0.3, "metadata": 0.3}

    def execute(self, query: SearchQuery, context: Dict[str, Any]) -> List[SearchResultItem]:
        em = context.get("embedding_manager")
        vdb = context.get("vector_db")
        if not em or not vdb:
            raise ValueError("Missing required dependencies in context")
        all_results: Dict[str, SearchResultItem] = {}
        if query.query:
            emb = em.get_text_embedding(query.query, "clip")
            for r in vdb.search(emb, k=query.limit * 2):
                all_results.setdefault(r.vector_id, r)
                all_results[r.vector_id].scores = getattr(all_results[r.vector_id], "scores", {})
                all_results[r.vector_id].scores["text"] = r.similarity_score
        if query.image_path:
            emb = em.get_image_embedding(query.image_path, "clip")
            for r in vdb.search(emb, k=query.limit * 2):
                all_results.setdefault(r.vector_id, r)
                all_results[r.vector_id].scores = getattr(all_results[r.vector_id], "scores", {})
                all_results[r.vector_id].scores["visual"] = r.similarity_score
        if query.filters:
            for r in all_results.values():
                r.scores["metadata"] = 1.0
        hybrid = []
        for r in all_results.values():
            r.similarity_score = self._calculate_hybrid_score(r.scores)
            hybrid.append(r)
        hybrid.sort(key=lambda x: x.similarity_score, reverse=True)
        final = hybrid[: query.limit]
        self._log_search(query, len(final))
        return final

    def _calculate_hybrid_score(self, scores: Dict[str, float]) -> float:
        total_s = total_w = 0.0
        for stype, weight in self._weights.items():
            if stype in scores:
                total_s += scores[stype] * weight
                total_w += weight
        return total_s / total_w if total_w > 0 else 0.0

    def validate_query(self, query: SearchQuery) -> tuple[bool, str]:
        if not query.query and not query.image_path:
            return False, "Either text query or image path is required"
        if query.image_path and not os.path.exists(query.image_path):
            return False, f"Image file not found: {query.image_path}"
        return True, "Valid"
