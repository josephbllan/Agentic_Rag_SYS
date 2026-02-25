from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from ..enums import QueryType
from .search_result_item import SearchResultItem
from .search_filters import SearchFilters


class SearchResponse(BaseModel):
    results: List[SearchResultItem]
    total_count: int = Field(..., ge=0)
    query_type: QueryType
    execution_time: float = Field(..., ge=0.0)
    query_metadata: Dict[str, Any] = Field(default_factory=dict)
    filters_applied: Optional[SearchFilters] = None

    class Config:
        use_enum_values = True
