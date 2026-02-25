"""
Dependency Injection for FastAPI
Thread-safe singleton instances for controllers and services.
"""
import threading
from typing import Optional

from core.vector_db import BaseVectorDB, create_vector_db
from core.search_engine import SearchEngine
from core.query_processor import QueryProcessor

_lock = threading.Lock()
_vector_db_instance: Optional[BaseVectorDB] = None
_search_engine_instance: Optional[SearchEngine] = None
_query_processor_instance: Optional[QueryProcessor] = None


def get_vector_db() -> BaseVectorDB:
    global _vector_db_instance
    if _vector_db_instance is None:
        with _lock:
            if _vector_db_instance is None:
                _vector_db_instance = create_vector_db()
    return _vector_db_instance


def get_search_engine() -> SearchEngine:
    global _search_engine_instance
    if _search_engine_instance is None:
        with _lock:
            if _search_engine_instance is None:
                _search_engine_instance = SearchEngine(vector_db=get_vector_db())
    return _search_engine_instance


def get_query_processor() -> QueryProcessor:
    global _query_processor_instance
    if _query_processor_instance is None:
        with _lock:
            if _query_processor_instance is None:
                _query_processor_instance = QueryProcessor()
    return _query_processor_instance


def reset_instances() -> None:
    """Reset all singletons (useful for testing)."""
    global _vector_db_instance, _search_engine_instance, _query_processor_instance
    with _lock:
        _vector_db_instance = None
        _search_engine_instance = None
        _query_processor_instance = None
