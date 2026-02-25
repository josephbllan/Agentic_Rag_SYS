"""Search logging and statistics gathering."""
import json
import logging
from typing import Dict, Any, Optional

from config.database import get_db_session, SearchQuery

logger = logging.getLogger(__name__)


def log_search_query(
    query: str,
    query_type: str,
    filters: Optional[Dict[str, Any]],
    result_count: int,
) -> None:
    """Persists a search query record to the database, silently logging
    any errors that occur during the write."""
    try:
        with get_db_session() as db:
            db.add(SearchQuery(
                query_text=query,
                query_type=query_type,
                filters=json.dumps(filters) if filters else None,
                results_count=result_count,
                execution_time=0.0,
            ))
    except Exception as e:
        logger.error(f"Failed to log search query: {e}")


def get_search_stats(vector_db) -> Dict[str, Any]:
    """Aggregates statistics from the most recent search queries and
    combines them with vector database stats."""
    try:
        with get_db_session() as db:
            recent = (
                db.query(SearchQuery)
                .order_by(SearchQuery.created_at.desc())
                .limit(100)
                .all()
            )
            total = len(recent)
            query_types: Dict[str, int] = {}
            avg_results = 0
            for s in recent:
                query_types[s.query_type] = query_types.get(s.query_type, 0) + 1
                avg_results += s.results_count or 0
            avg_results = avg_results / total if total else 0
            return {
                "total_searches": total,
                "query_types": query_types,
                "avg_results_per_search": avg_results,
                "vector_db_stats": vector_db.get_stats(),
            }
    except Exception as e:
        logger.error(f"Failed to get search stats: {e}")
        return {}
