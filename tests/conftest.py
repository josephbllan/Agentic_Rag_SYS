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
        self._dimension = dimension
        self._store: List[Dict[str, Any]] = []

    @property
    def dimension(self) -> int:
        return self._dimension

    def add_vectors(
        self,
        vectors: np.ndarray,
        metadata: List[Dict[str, Any]],
        ids: Optional[List[str]] = None,
    ) -> None:
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
        for entry in self._store:
            if entry.get("vector_id") == vector_id:
                return entry["_vec"]
        return None

    def update_metadata(self, vector_id: str, metadata: Dict[str, Any]) -> None:
        for entry in self._store:
            if entry.get("vector_id") == vector_id:
                entry.update(metadata)
                return

    def delete_vector(self, vector_id: str) -> None:
        self._store = [e for e in self._store if e.get("vector_id") != vector_id]

    def get_stats(self) -> Dict[str, Any]:
        return {"backend": "fake", "total_vectors": len(self._store)}

    def rebuild_index(self) -> None:
        pass

    def clear_database(self) -> None:
        self._store.clear()


@pytest.fixture
def fake_vector_db():
    return FakeVectorDB()


@pytest.fixture
def random_vectors():
    rng = np.random.default_rng(42)
    return rng.random((5, 512)).astype("float32")
