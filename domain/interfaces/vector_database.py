from typing import Protocol, List, Dict, Any, Optional, runtime_checkable
from ..types import VectorType
from ..models import SearchResultItem


@runtime_checkable
class IVectorDatabase(Protocol):
    def add_vectors(self, vectors: VectorType, metadata: List[Dict[str, Any]], ids: Optional[List[str]] = None) -> None:
        """Adds vectors with their associated metadata and optional identifiers."""
        ...

    def search(self, query_vector: VectorType, k: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[SearchResultItem]:
        """Searches for the k nearest vectors to the query vector with optional filters."""
        ...

    def delete_vector(self, vector_id: str) -> None:
        """Deletes a vector from the database by its unique identifier."""
        ...

    def get_stats(self) -> Dict[str, Any]:
        """Returns a dictionary of statistics about the vector database."""
        ...

    def rebuild_index(self) -> None:
        """Rebuilds the vector search index for improved query performance."""
        ...
