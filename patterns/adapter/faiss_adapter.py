from typing import List, Dict, Any, Optional
import logging
from domain.types import VectorType
from domain.models import SearchResultItem
from domain.base_classes import BaseVectorDatabase


class FAISSAdapter(BaseVectorDatabase):
    def __init__(self, dimension: int, collection_name: str = "default"):
        """Initializes the FAISS adapter with the specified dimension and collection name.
        Creates a flat L2 index for exact nearest-neighbor search.
        """
        super().__init__(dimension, collection_name)
        import faiss
        import numpy as np
        self._faiss = faiss
        self._np = np
        self._metadata = []
        self._index = self._faiss.IndexFlatL2(self._dimension)
        self._is_initialized = True

    def add_vectors(self, vectors: VectorType, metadata: List[Dict[str, Any]], ids: Optional[List[str]] = None) -> None:
        """Adds vectors and their associated metadata to the FAISS index.
        Vectors are cast to float32 before insertion.
        """
        self._index.add(vectors.astype("float32"))
        self._metadata.extend(metadata)

    def search(self, query_vector: VectorType, k: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[SearchResultItem]:
        """Searches the FAISS index for the k nearest neighbors of the query vector.
        Returns a list of SearchResultItem objects with inverse-distance similarity scores.
        """
        distances, indices = self._index.search(query_vector.reshape(1, -1).astype("float32"), k)
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self._metadata):
                meta = self._metadata[idx]
                results.append(SearchResultItem(
                    vector_id=meta.get("vector_id", f"idx_{idx}"),
                    filename=meta.get("filename", ""),
                    original_path=meta.get("original_path", ""),
                    similarity_score=1.0 / (1.0 + float(distance)),
                    rank=i + 1,
                    metadata=meta,
                ))
        return results

    def delete_vector(self, vector_id: str) -> None:
        """Marks a vector as deleted in the metadata store by setting a deletion flag.
        Does not remove the vector from the underlying FAISS index.
        """
        for meta in self._metadata:
            if meta.get("vector_id") == vector_id:
                meta["_deleted"] = True
                break

    def get_stats(self) -> Dict[str, Any]:
        """Returns statistics about the FAISS index including total vectors,
        dimension, and backend identifier.
        """
        return {"total_vectors": self._index.ntotal, "dimension": self._dimension, "backend": "faiss"}
