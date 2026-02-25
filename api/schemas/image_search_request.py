from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class ImageSearchRequest(BaseModel):
    image_path: str = Field(..., description="Path to reference image")
    filters: Optional[Dict[str, Any]] = Field(None, description="Metadata filters")
    limit: int = Field(10, gt=0, le=100, description="Maximum number of results")
    similarity_threshold: float = Field(0.7, ge=0.0, le=1.0, description="Minimum similarity score")
