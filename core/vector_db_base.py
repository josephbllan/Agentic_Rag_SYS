"""Abstract base class for vector database backends."""
import numpy as np
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod


class BaseVectorDB(ABC):
    """Abstract base for vector database backends."""

    def __init__(self, dimension: int, collection_name: str = "shoe_images"):
        """Stores the vector dimension and collection name for use by
        concrete backend implementations."""
        self._dimension = dimension
        self._collection_name = collection_name

    @property
    def dimension(self) -> int:
        """Returns the dimensionality of vectors stored in this database."""
        return self._dimension

    @property
    def collection_name(self) -> str:
        """Returns the name of the vector collection managed by this instance."""
        return self._collection_name

    @abstractmethod
    def add_vectors(
        self, vectors: np.ndarray, metadata: List[Dict[str, Any]],
        ids: Optional[List[str]] = None,
    ) -> None:
        """Adds embedding vectors with associated metadata to the database."""
        ...

    @abstractmethod
    def search(
        self, query_vector: np.ndarray, k: int = 10,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Searches for the k nearest vectors, optionally filtered by metadata."""
        ...

    @abstractmethod
    def get_vector_by_id(self, vector_id: str) -> Optional[np.ndarray]:
        """Retrieves a single vector by its unique identifier."""
        ...

    @abstractmethod
    def update_metadata(self, vector_id: str, metadata: Dict[str, Any]) -> None:
        """Updates the metadata associated with the given vector ID."""
        ...

    @abstractmethod
    def delete_vector(self, vector_id: str) -> None:
        """Removes a vector and its metadata from the database."""
        ...

    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:
        """Returns a dictionary of backend-specific database statistics."""
        ...

    @abstractmethod
    def rebuild_index(self) -> None:
        """Rebuilds the search index to reflect any pending changes."""
        ...

    @abstractmethod
    def clear_database(self) -> None:
        """Removes all vectors and metadata, resetting the database."""
        ...

    @staticmethod
    def _apply_filters(
        results: List[Dict[str, Any]], filters: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Filters a list of result dictionaries, keeping only those whose
        metadata values match all specified filter criteria."""
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
