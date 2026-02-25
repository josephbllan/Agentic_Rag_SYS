from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class HybridSearchRequest(BaseModel):
    query: Optional[str] = Field(None, description="Text query")
    image_path: Optional[str] = Field(None, description="Path to reference image")
    filters: Optional[Dict[str, Any]] = Field(None, description="Metadata filters")
    limit: int = Field(10, gt=0, le=100, description="Maximum number of results")
