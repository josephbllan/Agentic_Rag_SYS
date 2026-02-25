"""Abstract base class for vector database backends."""
import numpy as np
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod


class BaseVectorDB(ABC):
    """Abstract base for vector database backends."""

    def __init__(self, dimension: int, collection_name: str = "shoe_images"):
        self._dimension = dimension
        self._collection_name = collection_name

    @property
    def dimension(self) -> int:
        return self._dimension

    @property
    def collection_name(self) -> str:
        return self._collection_name

    @abstractmethod
    def add_vectors(
        self, vectors: np.ndarray, metadata: List[Dict[str, Any]],
        ids: Optional[List[str]] = None,
    ) -> None: ...

    @abstractmethod
    def search(
        self, query_vector: np.ndarray, k: int = 10,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]: ...

    @abstractmethod
    def get_vector_by_id(self, vector_id: str) -> Optional[np.ndarray]: ...

    @abstractmethod
    def update_metadata(self, vector_id: str, metadata: Dict[str, Any]) -> None: ...

    @abstractmethod
    def delete_vector(self, vector_id: str) -> None: ...

    @abstractmethod
    def get_stats(self) -> Dict[str, Any]: ...

    @abstractmethod
    def rebuild_index(self) -> None: ...

    @abstractmethod
    def clear_database(self) -> None: ...

    @staticmethod
    def _apply_filters(
        results: List[Dict[str, Any]], filters: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        filtered = []
        for result in results:
            match = True
            for key, value in filters.items():
                if key not in result:
                    match = False
                    break
                if isinstance(value, list):
                    if result[key] not in value:
                        match = False
                        break
                elif result[key] != value:
                    match = False
                    break
            if match:
                filtered.append(result)
        return filtered
