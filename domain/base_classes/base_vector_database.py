from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import logging
from ..types import VectorType
from ..models import SearchResultItem


class BaseVectorDatabase(ABC):
    def __init__(self, dimension: int, collection_name: str = "default"):
        """Initializes the vector database with the given vector dimension and collection name.
        Sets up logging and marks the database as not yet initialized.
        """
        self._dimension = dimension
        self._collection_name = collection_name
        self._logger = logging.getLogger(self.__class__.__name__)
        self._is_initialized = False

    @property
    def dimension(self) -> int:
        """Returns the dimensionality of vectors stored in this database."""
        return self._dimension

    @property
    def collection_name(self) -> str:
        """Returns the name of the vector collection managed by this database."""
        return self._collection_name

    @property
    def is_initialized(self) -> bool:
        """Indicates whether the vector database has been initialized and is ready."""
        return self._is_initialized

    @abstractmethod
    def add_vectors(self, vectors: VectorType, metadata: List[Dict[str, Any]], ids: Optional[List[str]] = None) -> None:
        """Adds vectors with their associated metadata to the database.
        Optionally accepts explicit identifiers for each vector.
        """
        pass

    @abstractmethod
    def search(self, query_vector: VectorType, k: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[SearchResultItem]:
        """Searches for the k nearest vectors to the query vector.
        Optionally applies metadata filters to narrow the results.
        """
        pass

    @abstractmethod
    def delete_vector(self, vector_id: str) -> None:
        """Deletes a vector from the database by its unique identifier."""
        pass

    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:
        """Returns a dictionary of statistics about the vector database."""
        pass

    def rebuild_index(self) -> None:
        """Rebuilds the vector index if supported by the implementation.
        Logs a warning by default since not all backends support this operation.
        """
        self._logger.warning(f"{self.__class__.__name__} does not support index rebuilding")

    def __repr__(self) -> str:
        """Returns a string representation including dimension and collection name."""
        return f"{self.__class__.__name__}(dimension={self._dimension}, collection='{self._collection_name}')"
