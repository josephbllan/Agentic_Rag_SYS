from typing import List, Dict, Any, Optional
import logging
from domain.types import VectorType
from domain.models import SearchResultItem
from domain.base_classes import BaseVectorDatabase


class VectorDatabaseAdapter:
    def __init__(self, database: BaseVectorDatabase):
        """Initializes the adapter with a reference to the underlying vector database
        and configures a logger for this instance.
        """
        self._database = database
        self._logger = logging.getLogger(self.__class__.__name__)

    def add(self, vectors: VectorType, metadata: List[Dict[str, Any]], ids: Optional[List[str]] = None) -> None:
        """Delegates vector addition to the underlying database implementation."""
        self._database.add_vectors(vectors, metadata, ids)

    def search(self, query: VectorType, limit: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[SearchResultItem]:
        """Delegates search queries to the underlying database with the specified limit and filters."""
        return self._database.search(query, k=limit, filters=filters)

    def remove(self, vector_id: str) -> None:
        """Delegates vector deletion to the underlying database by vector ID."""
        self._database.delete_vector(vector_id)

    def statistics(self) -> Dict[str, Any]:
        """Retrieves and returns statistics from the underlying database implementation."""
        return self._database.get_stats()
