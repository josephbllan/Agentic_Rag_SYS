"""FAISS-backed vector database implementation."""
import pickle
import logging
import numpy as np
from typing import List, Dict, Any, Optional

import faiss

from config.settings import VECTOR_DB_DIR, VECTOR_DB_CONFIG
from core.vector_db_base import BaseVectorDB

logger = logging.getLogger(__name__)


class FAISSVectorDB(BaseVectorDB):
    """FAISS-backed vector database."""

    def __init__(self, dimension: int, collection_name: str = "shoe_images"):
        """Initializes the FAISS index paths and loads or creates the
        underlying index and metadata store."""
        super().__init__(dimension, collection_name)
        self._index_path = VECTOR_DB_DIR / f"{collection_name}.faiss"
        self._meta_path = VECTOR_DB_DIR / f"{collection_name}_metadata.pkl"
        self._load_or_create()

    def _load_or_create(self) -> None:
        """Loads an existing FAISS index and metadata from disk, or creates
        a new IVFFlat index if no persisted data is found."""
        if self._index_path.exists() and self._meta_path.exists():
            self.index = faiss.read_index(str(self._index_path))
            with open(self._meta_path, "rb") as f:
                self.metadata: List[Dict[str, Any]] = pickle.load(f)
        else:
            nlist = VECTOR_DB_CONFIG["faiss"]["nlist"]
            self.index = faiss.IndexIVFFlat(
                faiss.IndexFlatL2(self._dimension), self._dimension, nlist
            )
            self.metadata = []

    def add_vectors(
        self, vectors: np.ndarray, metadata: List[Dict[str, Any]],
        ids: Optional[List[str]] = None,
    ) -> None:
        """Trains the index if needed, adds vectors with metadata,
        and persists the updated index to disk."""
        vecs = vectors.astype("float32")
        if not self.index.is_trained:
            self.index.train(vecs[: min(1000, len(vecs))])
        self.index.add(vecs)
        if ids is None:
            ids = [f"item_{len(self.metadata) + i}" for i in range(len(vecs))]
        for i, (vid, meta) in enumerate(zip(ids, metadata)):
            meta["vector_id"] = vid
            meta["index_id"] = len(self.metadata) + i
            self.metadata.append(meta)
        self._persist()

    def update_metadata(self, vector_id: str, metadata: Dict[str, Any]) -> None:
        """Updates the metadata dictionary for the vector matching the given ID
        and persists the changes to disk."""
        for i, meta in enumerate(self.metadata):
            if meta.get("vector_id") == vector_id:
                self.metadata[i].update(metadata)
                self._persist()
                return

    def delete_vector(self, vector_id: str) -> None:
        """Soft-deletes a vector by marking its metadata entry as deleted
        rather than removing it from the FAISS index."""
        for meta in self.metadata:
            if meta.get("vector_id") == vector_id:
                meta["deleted"] = True
                self._persist()
                return

    def search(
        self, query_vector: np.ndarray, k: int = 10,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Searches the FAISS index for the k nearest neighbors and returns
        ranked results with similarity scores, optionally filtered by metadata."""
        self.index.nprobe = VECTOR_DB_CONFIG["faiss"]["nprobe"]
        distances, indices = self.index.search(
            query_vector.reshape(1, -1).astype("float32"), k
        )
        results = []
        for rank, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.metadata):
                result = self.metadata[idx].copy()
                result["similarity_score"] = 1.0 / (1.0 + distance)
                result["rank"] = rank + 1
                results.append(result)
        if filters:
            results = self._apply_filters(results, filters)
        return results

    def get_vector_by_id(self, vector_id: str) -> Optional[np.ndarray]:
        """Returns None as FAISS does not natively support retrieval
        of individual vectors by ID."""
        return None

    def get_stats(self) -> Dict[str, Any]:
        """Returns a dictionary of index statistics including total vectors,
        dimension, training state, and metadata count."""
        return {
            "backend": "faiss",
            "total_vectors": self.index.ntotal,
            "dimension": self.index.d,
            "is_trained": self.index.is_trained,
            "metadata_count": len(self.metadata),
        }

    def rebuild_index(self) -> None:
        """Rebuilds the FAISS index by removing soft-deleted metadata entries
        and reinitializing the underlying IVFFlat structure."""
        valid = [m for m in self.metadata if not m.get("deleted", False)]
        if not valid:
            return
        nlist = VECTOR_DB_CONFIG["faiss"]["nlist"]
        self.index = faiss.IndexIVFFlat(
            faiss.IndexFlatL2(self._dimension), self._dimension, nlist
        )
        logger.info("Rebuild requires re-embedding; metadata-only reset")
        self.metadata = valid
        self._persist()

    def clear_database(self) -> None:
        """Replaces the current index with a fresh empty IVFFlat index
        and clears all stored metadata."""
        nlist = VECTOR_DB_CONFIG["faiss"]["nlist"]
        self.index = faiss.IndexIVFFlat(
            faiss.IndexFlatL2(self._dimension), self._dimension, nlist
        )
        self.metadata = []
        self._persist()

    def _persist(self) -> None:
        """Writes the FAISS index and metadata to their respective files
        on disk for persistence."""
        faiss.write_index(self.index, str(self._index_path))
        with open(self._meta_path, "wb") as f:
            pickle.dump(self.metadata, f)
