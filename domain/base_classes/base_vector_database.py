from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import logging
from ..types import VectorType
from ..models import SearchResultItem


class BaseVectorDatabase(ABC):
    def __init__(self, dimension: int, collection_name: str = "default"):
        self._dimension = dimension
        self._collection_name = collection_name
        self._logger = logging.getLogger(self.__class__.__name__)
        self._is_initialized = False

    @property
    def dimension(self) -> int:
        return self._dimension

    @property
    def collection_name(self) -> str:
        return self._collection_name

    @property
    def is_initialized(self) -> bool:
        return self._is_initialized

    @abstractmethod
    def add_vectors(self, vectors: VectorType, metadata: List[Dict[str, Any]], ids: Optional[List[str]] = None) -> None:
        pass

    @abstractmethod
    def search(self, query_vector: VectorType, k: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[SearchResultItem]:
        pass

    @abstractmethod
    def delete_vector(self, vector_id: str) -> None:
        pass

    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:
        pass

    def rebuild_index(self) -> None:
        self._logger.warning(f"{self.__class__.__name__} does not support index rebuilding")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(dimension={self._dimension}, collection='{self._collection_name}')"
