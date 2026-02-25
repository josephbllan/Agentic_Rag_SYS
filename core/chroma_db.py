"""ChromaDB-backed vector database implementation."""
import logging
import numpy as np
from typing import List, Dict, Any, Optional

import chromadb
from chromadb.config import Settings

from config.settings import VECTOR_DB_DIR, VECTOR_DB_CONFIG
from core.vector_db_base import BaseVectorDB

logger = logging.getLogger(__name__)


class ChromaVectorDB(BaseVectorDB):
    """ChromaDB-backed vector database."""

    def __init__(self, dimension: int, collection_name: str = "shoe_images"):
        super().__init__(dimension, collection_name)
        self._client = chromadb.Client(
            Settings(persist_directory=str(VECTOR_DB_DIR / "chroma_db"))
        )
        self._ensure_collection()

    def _ensure_collection(self) -> None:
        try:
            self.collection = self._client.get_collection(self._collection_name)
        except ValueError:
            self.collection = self._client.create_collection(
                name=self._collection_name,
                metadata={"hnsw:space": VECTOR_DB_CONFIG["chroma"]["distance_metric"]},
            )

    def add_vectors(
        self, vectors: np.ndarray, metadata: List[Dict[str, Any]],
        ids: Optional[List[str]] = None,
    ) -> None:
        if ids is None:
            ids = [f"item_{i}" for i in range(len(vectors))]
        self.collection.add(embeddings=vectors.tolist(), metadatas=metadata, ids=ids)

    def update_metadata(self, vector_id: str, metadata: Dict[str, Any]) -> None:
        self.collection.update(ids=[vector_id], metadatas=[metadata])

    def delete_vector(self, vector_id: str) -> None:
        self.collection.delete(ids=[vector_id])

    def search(
        self, query_vector: np.ndarray, k: int = 10,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        where_clause: Dict[str, Any] = {}
        if filters:
            for key, value in filters.items():
                where_clause[key] = {"$in": value} if isinstance(value, list) else value
        results = self.collection.query(
            query_embeddings=[query_vector.tolist()],
            n_results=k,
            where=where_clause if where_clause else None,
        )
        formatted: List[Dict[str, Any]] = []
        for rank, (vid, dist, meta) in enumerate(
            zip(results["ids"][0], results["distances"][0], results["metadatas"][0])
        ):
            entry = meta.copy()
            entry["vector_id"] = vid
            entry["similarity_score"] = 1.0 - dist
            entry["rank"] = rank + 1
            formatted.append(entry)
        return formatted

    def get_vector_by_id(self, vector_id: str) -> Optional[np.ndarray]:
        result = self.collection.get(ids=[vector_id])
        if result["embeddings"]:
            return np.array(result["embeddings"][0])
        return None

    def get_stats(self) -> Dict[str, Any]:
        return {
            "backend": "chroma",
            "total_vectors": self.collection.count(),
            "collection_name": self._collection_name,
        }

    def rebuild_index(self) -> None:
        logger.warning("ChromaDB manages its own index; rebuild is a no-op")

    def clear_database(self) -> None:
        self._client.delete_collection(self._collection_name)
        self.collection = self._client.create_collection(
            name=self._collection_name,
            metadata={"hnsw:space": VECTOR_DB_CONFIG["chroma"]["distance_metric"]},
        )
