import re
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from ..enums import QueryType
from .search_filters import SearchFilters


class SearchQuery(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    query_type: QueryType = QueryType.TEXT
    filters: Optional[SearchFilters] = None
    limit: int = Field(10, gt=0, le=100)
    similarity_threshold: float = Field(0.7, ge=0.0, le=1.0)
    image_path: Optional[str] = None
    session_id: Optional[str] = None
    user_id: Optional[str] = None

    @validator('query')
    def sanitize_query(cls, v: str) -> str:
        malicious_patterns = [
            r'<script', r'javascript:', r'on\w+=',
            r'eval\(', r'exec\(',
        ]
        for pattern in malicious_patterns:
            if re.search(pattern, v, re.IGNORECASE):
                raise ValueError('Query contains potentially malicious content')
        return v.strip()

    @validator('image_path')
    def validate_image_path(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v or '..' in v:
                raise ValueError('Invalid image path')
        return v

    class Config:
        use_enum_values = True
        validate_assignment = True
