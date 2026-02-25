from typing import List, Dict, Any
from domain.models import SearchQuery, SearchResultItem
from domain.base_classes import BaseSearchStrategy


class SemanticSearchStrategy(BaseSearchStrategy):
    def __init__(self):
        super().__init__(name="semantic_search")

    def execute(self, query: SearchQuery, context: Dict[str, Any]) -> List[SearchResultItem]:
        em = context.get("embedding_manager")
        vdb = context.get("vector_db")
        qp = context.get("query_processor")
        if not all([em, vdb, qp]):
            raise ValueError("Missing required dependencies in context")
        expanded = qp.expand_query(query.query)
        all_results: Dict[str, SearchResultItem] = {}
        for eq in expanded:
            emb = em.get_text_embedding(eq, "clip")
            for r in vdb.search(emb, k=query.limit * 2):
                all_results.setdefault(r.vector_id, r)
                all_results[r.vector_id].scores = getattr(all_results[r.vector_id], "scores", {"matches": 0})
                all_results[r.vector_id].scores["matches"] += 1
        sem = []
        for r in all_results.values():
            boost = min(r.scores.get("matches", 0) * 0.1, 0.3)
            r.similarity_score = min(r.similarity_score + boost, 1.0)
            sem.append(r)
        sem.sort(key=lambda x: x.similarity_score, reverse=True)
        final = sem[: query.limit]
        self._log_search(query, len(final))
        return final

    def validate_query(self, query: SearchQuery) -> tuple[bool, str]:
        if not query.query or not query.query.strip():
            return False, "Query is empty"
        return True, "Valid"
