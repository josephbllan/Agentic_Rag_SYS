from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class TextSearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500, description="Search query text")
    filters: Optional[Dict[str, Any]] = Field(None, description="Metadata filters")
    limit: int = Field(10, gt=0, le=100, description="Maximum number of results")
    similarity_threshold: float = Field(0.7, ge=0.0, le=1.0, description="Minimum similarity score")
