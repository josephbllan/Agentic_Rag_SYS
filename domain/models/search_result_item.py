from typing import Optional, Dict
from pydantic import BaseModel, Field
from .image_metadata import ImageMetadata


class SearchResultItem(BaseModel):
    vector_id: str
    filename: str
    original_path: str
    similarity_score: float = Field(..., ge=0.0, le=1.0)
    rank: int = Field(..., gt=0)
    metadata: ImageMetadata
    scores: Optional[Dict[str, float]] = Field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True
