"""
Shared pytest fixtures for the RAG system test suite.
"""
import sys
import os
from pathlib import Path
from unittest.mock import MagicMock, patch
from typing import List, Dict, Any, Optional

import numpy as np
import pytest

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ---------------------------------------------------------------------------
# Fake / stub implementations used across tests
# ---------------------------------------------------------------------------

class FakeVectorDB:
    """In-memory vector DB stub that satisfies BaseVectorDB interface."""

    def __init__(self, dimension: int = 512):
        """Initializes the fake vector database with the given
        embedding dimension and an empty in-memory store.
        """
        self._dimension = dimension
        self._store: List[Dict[str, Any]] = []

    @property
    def dimension(self) -> int:
        """Returns the configured embedding dimension."""
        return self._dimension

    def add_vectors(
        self,
        vectors: np.ndarray,
        metadata: List[Dict[str, Any]],
        ids: Optional[List[str]] = None,
    ) -> None:
        """Stores vectors and their metadata in the in-memory list,
        auto-generating IDs if none are provided.
        """
        if ids is None:
            ids = [f"fake_{len(self._store) + i}" for i in range(len(vectors))]
        for vid, vec, meta in zip(ids, vectors, metadata):
            entry = meta.copy()
            entry["vector_id"] = vid
            entry["_vec"] = vec
            self._store.append(entry)

    def search(
        self,
        query_vector: np.ndarray,
        k: int = 10,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Performs a brute-force nearest-neighbour search over stored
        vectors, applies optional filters, and returns the top-k results.
        """
        results = []
        qv = query_vector.flatten().astype("float32")
        for entry in self._store:
            ev = entry["_vec"].flatten().astype("float32")
            dist = float(np.linalg.norm(qv - ev))
            result = {k2: v for k2, v in entry.items() if k2 != "_vec"}
            result["similarity_score"] = 1.0 / (1.0 + dist)
            results.append(result)
        results.sort(key=lambda r: r["similarity_score"], reverse=True)
        if filters:
            results = [r for r in results if all(r.get(fk) == fv for fk, fv in filters.items())]
        return results[:k]

    def get_vector_by_id(self, vector_id: str) -> Optional[np.ndarray]:
        """Looks up and returns the raw vector for the given ID, or None if not found."""
        for entry in self._store:
            if entry.get("vector_id") == vector_id:
                return entry["_vec"]
        return None

    def update_metadata(self, vector_id: str, metadata: Dict[str, Any]) -> None:
        """Updates the metadata dict for the entry matching the given vector ID."""
        for entry in self._store:
            if entry.get("vector_id") == vector_id:
                entry.update(metadata)
                return

    def delete_vector(self, vector_id: str) -> None:
        """Removes the vector entry with the specified ID from the store."""
        self._store = [e for e in self._store if e.get("vector_id") != vector_id]

    def get_stats(self) -> Dict[str, Any]:
        """Returns basic statistics about the fake vector store."""
        return {"backend": "fake", "total_vectors": len(self._store)}

    def rebuild_index(self) -> None:
        """No-op for the fake backend; satisfies the interface contract."""
        pass

    def clear_database(self) -> None:
        """Empties all stored vectors and metadata from memory."""
        self._store.clear()


@pytest.fixture
def fake_vector_db():
    """Provides a fresh FakeVectorDB instance for each test."""
    return FakeVectorDB()


@pytest.fixture
def random_vectors():
    """Generates a deterministic 5x512 float32 array of random vectors for testing."""
    rng = np.random.default_rng(42)
    return rng.random((5, 512)).astype("float32")
