"""Main Search Engine for RAG System.
Dependencies are injected for testability.
"""
import numpy as np
from typing import List, Dict, Any, Optional
import logging

from core.vector_db import BaseVectorDB, create_vector_db
from core.embeddings import EmbeddingManager, MultiModalEmbedder, cosine_similarity
from core.search_analytics import log_search_query, get_search_stats
from config.settings import SEARCH_CONFIG

logger = logging.getLogger(__name__)


class SearchEngine:
    """Main search engine with constructor-injected dependencies."""

    def __init__(
        self,
        vector_db: Optional[BaseVectorDB] = None,
        embedding_manager: Optional[EmbeddingManager] = None,
        multimodal_embedder: Optional[MultiModalEmbedder] = None,
        *,
        vector_backend: str = "faiss",
    ):
        self.vector_db = vector_db or create_vector_db(vector_backend)
        self.embedding_manager = embedding_manager or EmbeddingManager()
        self.multimodal_embedder = multimodal_embedder or MultiModalEmbedder()
        self.max_results = SEARCH_CONFIG["max_results"]
        self.similarity_threshold = SEARCH_CONFIG["similarity_threshold"]
        self.hybrid_weights = SEARCH_CONFIG["hybrid_weights"]

    def text_to_image_search(
        self, query: str, filters: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        try:
            emb = self.embedding_manager.get_text_embedding(query, "clip")
            limit = limit or self.max_results
            results = self.vector_db.search(emb, k=limit, filters=filters)
            results = [r for r in results if r.get("similarity_score", 0) >= self.similarity_threshold]
            log_search_query(query, "text", filters, len(results))
            return results
        except Exception as e:
            logger.error(f"Text-to-image search failed: {e}")
            return []

    def image_to_image_search(
        self, image_path: str, filters: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        try:
            emb = self.embedding_manager.get_image_embedding(image_path, "clip")
            limit = limit or self.max_results
            results = self.vector_db.search(emb, k=limit, filters=filters)
            results = [r for r in results if r.get("similarity_score", 0) >= self.similarity_threshold]
            log_search_query(f"Image: {image_path}", "image", filters, len(results))
            return results
        except Exception as e:
            logger.error(f"Image-to-image search failed: {e}")
            return []

    def metadata_search(
        self, filters: Dict[str, Any], limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        try:
            limit = limit or self.max_results
            results = self.vector_db.search(np.zeros(512), k=1000, filters=filters)
            results = results[:limit]
            log_search_query("Metadata filter", "metadata", filters, len(results))
            return results
        except Exception as e:
            logger.error(f"Metadata search failed: {e}")
            return []

    def hybrid_search(
        self, query: Optional[str] = None, image_path: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None, limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        try:
            limit = limit or self.max_results
            all_results: Dict[Any, Dict[str, Any]] = {}
            if query:
                for r in self.text_to_image_search(query, filters, limit):
                    rid = r.get("vector_id", r.get("index_id"))
                    all_results.setdefault(rid, {**r, "scores": {}})
                    all_results[rid]["scores"]["text"] = r.get("similarity_score", 0)
            if image_path:
                for r in self.image_to_image_search(image_path, filters, limit):
                    rid = r.get("vector_id", r.get("index_id"))
                    all_results.setdefault(rid, {**r, "scores": {}})
                    all_results[rid]["scores"]["visual"] = r.get("similarity_score", 0)
            if filters:
                for r in self.metadata_search(filters, limit):
                    rid = r.get("vector_id", r.get("index_id"))
                    all_results.setdefault(rid, {**r, "scores": {}})
                    all_results[rid]["scores"]["metadata"] = 1.0
            hybrid = []
            for r in all_results.values():
                r["hybrid_score"] = self._hybrid_score(r.get("scores", {}))
                hybrid.append(r)
            hybrid.sort(key=lambda x: x.get("hybrid_score", 0), reverse=True)
            final = hybrid[:limit]
            log_search_query(f"Q:{query} I:{image_path}", "hybrid", filters, len(final))
            return final
        except Exception as e:
            logger.error(f"Hybrid search failed: {e}")
            return []

    def semantic_search(
        self, query: str, filters: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        try:
            expanded = self._expand_query(query)
            all_results: Dict[Any, Dict[str, Any]] = {}
            for eq in expanded:
                for r in self.text_to_image_search(eq, filters, limit):
                    rid = r.get("vector_id", r.get("index_id"))
                    all_results.setdefault(rid, {**r, "query_matches": []})
                    all_results[rid]["query_matches"].append(eq)
            sem = []
            for r in all_results.values():
                boost = len(r.get("query_matches", [])) * 0.1
                r["semantic_score"] = r.get("similarity_score", 0) + boost
                sem.append(r)
            sem.sort(key=lambda x: x.get("semantic_score", 0), reverse=True)
            final = sem[: limit or self.max_results]
            log_search_query(f"Semantic: {query}", "semantic", filters, len(final))
            return final
        except Exception as e:
            logger.error(f"Semantic search failed: {e}")
            return []

    def get_recommendations(self, image_path: str, limit: int = 10) -> List[Dict[str, Any]]:
        try:
            recs = [
                r for r in self.image_to_image_search(image_path, limit=limit * 2)
                if r.get("original_path") != image_path
            ]
            return recs[:limit]
        except Exception as e:
            logger.error(f"Recommendations failed: {e}")
            return []

    def search_by_similarity(
        self, reference_image_path: str, similarity_threshold: float = 0.8,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        try:
            emb = self.embedding_manager.get_image_embedding(reference_image_path, "clip")
            results = self.vector_db.search(emb, k=limit or self.max_results)
            return [r for r in results if r.get("similarity_score", 0) >= similarity_threshold]
        except Exception as e:
            logger.error(f"Similarity search failed: {e}")
            return []

    def get_search_stats(self) -> Dict[str, Any]:
        return get_search_stats(self.vector_db)

    def _hybrid_score(self, scores: Dict[str, float]) -> float:
        total_s = total_w = 0.0
        for stype, weight in self.hybrid_weights.items():
            if stype in scores:
                total_s += scores[stype] * weight
                total_w += weight
        return total_s / total_w if total_w > 0 else 0.0

    def _expand_query(self, query: str) -> List[str]:
        exp = [query]
        q = query.lower()
        if "shoe" in q:
            exp.extend([query.replace("shoe", "sneaker"), query.replace("shoe", "footwear")])
        if "red" in q:
            exp.append(query.replace("red", "crimson"))
        if "nike" in q:
            exp.append(query.replace("nike", "nike air"))
        return exp


def create_search_engine(vector_backend: str = "faiss") -> SearchEngine:
    return SearchEngine(vector_backend=vector_backend)
