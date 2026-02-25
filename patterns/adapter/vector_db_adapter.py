from typing import List, Dict, Any, Optional
import logging
from domain.types import VectorType
from domain.models import SearchResultItem
from domain.base_classes import BaseVectorDatabase


class VectorDatabaseAdapter:
    def __init__(self, database: BaseVectorDatabase):
        self._database = database
        self._logger = logging.getLogger(self.__class__.__name__)

    def add(self, vectors: VectorType, metadata: List[Dict[str, Any]], ids: Optional[List[str]] = None) -> None:
        self._database.add_vectors(vectors, metadata, ids)

    def search(self, query: VectorType, limit: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[SearchResultItem]:
        return self._database.search(query, k=limit, filters=filters)

    def remove(self, vector_id: str) -> None:
        self._database.delete_vector(vector_id)

    def statistics(self) -> Dict[str, Any]:
        return self._database.get_stats()
