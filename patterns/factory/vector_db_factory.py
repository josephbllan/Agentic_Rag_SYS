from typing import Dict, Type
import logging
from domain.base_classes import BaseVectorDatabase


class VectorDatabaseFactory:
    _db_classes: Dict[str, Type[BaseVectorDatabase]] = {}
    _logger = logging.getLogger("VectorDatabaseFactory")

    @classmethod
    def register_database(cls, backend: str, db_class: Type[BaseVectorDatabase]) -> None:
        """Registers a vector database class under the given backend identifier."""
        cls._db_classes[backend] = db_class

    @classmethod
    def create_database(cls, backend: str, dimension: int, collection_name: str = "default", **kwargs) -> BaseVectorDatabase:
        """Creates and returns a vector database instance for the specified backend.
        Raises ValueError if the backend has not been registered.
        """
        if backend not in cls._db_classes:
            raise ValueError(f"Unknown backend: {backend}. Available: {list(cls._db_classes.keys())}")
        return cls._db_classes[backend](dimension=dimension, collection_name=collection_name, **kwargs)

    @classmethod
    def get_supported_backends(cls) -> list[str]:
        """Returns a list of all registered backend identifiers."""
        return list(cls._db_classes.keys())

    @classmethod
    def create_faiss_database(cls, dimension: int, collection_name: str = "default", **kw) -> BaseVectorDatabase:
        """Creates and returns a FAISS vector database with the specified dimension and collection."""
        return cls.create_database("faiss", dimension, collection_name, **kw)

    @classmethod
    def create_chroma_database(cls, dimension: int, collection_name: str = "default", **kw) -> BaseVectorDatabase:
        """Creates and returns a ChromaDB vector database with the specified dimension and collection."""
        return cls.create_database("chroma", dimension, collection_name, **kw)
