from typing import List, Dict, Any, Optional
from domain.types import VectorType
from domain.models import SearchResultItem
from domain.base_classes import BaseVectorDatabase


class ChromaDBAdapter(BaseVectorDatabase):
    def __init__(self, dimension: int, collection_name: str = "default"):
        super().__init__(dimension, collection_name)
        import chromadb
        self._client = chromadb.Client()
        self._collection = self._client.get_or_create_collection(self._collection_name)
        self._is_initialized = True

    def add_vectors(self, vectors: VectorType, metadata: List[Dict[str, Any]], ids: Optional[List[str]] = None) -> None:
        if ids is None:
            ids = [f"id_{i}" for i in range(len(vectors))]
        self._collection.add(embeddings=vectors.tolist(), metadatas=metadata, ids=ids)

    def search(self, query_vector: VectorType, k: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[SearchResultItem]:
        results_data = self._collection.query(query_embeddings=[query_vector.tolist()], n_results=k)
        results = []
        for i, (vid, dist, meta) in enumerate(zip(results_data["ids"][0], results_data["distances"][0], results_data["metadatas"][0])):
            results.append(SearchResultItem(
                vector_id=vid,
                filename=meta.get("filename", ""),
                original_path=meta.get("original_path", ""),
                similarity_score=1.0 - float(dist),
                rank=i + 1,
                metadata=meta,
            ))
        return results

    def delete_vector(self, vector_id: str) -> None:
        self._collection.delete(ids=[vector_id])

    def get_stats(self) -> Dict[str, Any]:
        return {"total_vectors": self._collection.count(), "dimension": self._dimension, "backend": "chroma"}
