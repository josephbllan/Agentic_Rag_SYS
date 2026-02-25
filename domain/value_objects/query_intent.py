from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from ..enums import QueryType


@dataclass(frozen=True)
class QueryIntent:
    query_type: QueryType
    search_terms: List[str]
    filters: Dict[str, Any]
    image_path: Optional[str] = None
    similarity_threshold: float = 0.7
    limit: int = 10
    confidence: float = 1.0

    def __post_init__(self):
        if not 0.0 <= self.similarity_threshold <= 1.0:
            raise ValueError("similarity_threshold must be between 0 and 1")
        if self.limit < 1:
            raise ValueError("limit must be positive")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query_type": self.query_type.value,
            "search_terms": self.search_terms,
            "filters": self.filters,
            "image_path": self.image_path,
            "similarity_threshold": self.similarity_threshold,
            "limit": self.limit,
            "confidence": self.confidence,
        }
