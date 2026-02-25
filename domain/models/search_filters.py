from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field
from ..enums import BrandType, PatternType, ShapeType, SizeType


class SearchFilters(BaseModel):
    brand: Optional[Union[BrandType, List[BrandType]]] = None
    pattern: Optional[Union[PatternType, List[PatternType]]] = None
    shape: Optional[Union[ShapeType, List[ShapeType]]] = None
    size: Optional[Union[SizeType, List[SizeType]]] = None
    color: Optional[Union[str, List[str]]] = None
    style: Optional[Union[str, List[str]]] = None
    min_similarity: Optional[float] = Field(None, ge=0.0, le=1.0)
    max_results: Optional[int] = Field(None, gt=0, le=1000)

    def to_dict(self) -> Dict[str, Any]:
        """Converts the filters to a dictionary, excluding any fields set to None."""
        return {k: v for k, v in self.dict().items() if v is not None}

    class Config:
        use_enum_values = True
