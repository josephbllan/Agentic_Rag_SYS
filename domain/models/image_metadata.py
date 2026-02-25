from typing import Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field, validator, constr
from ..enums import PatternType, ShapeType, SizeType, BrandType


class ImageMetadata(BaseModel):
    filename: constr(min_length=1, max_length=255)
    original_path: str
    pattern: PatternType = PatternType.OTHER
    shape: ShapeType = ShapeType.ROUND
    size: SizeType = SizeType.MEDIUM
    brand: BrandType = BrandType.OTHER
    color: Optional[str] = None
    style: Optional[str] = None
    image_width: Optional[int] = Field(None, gt=0, le=10000)
    image_height: Optional[int] = Field(None, gt=0, le=10000)
    file_size: Optional[int] = Field(None, gt=0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @validator('filename')
    def validate_filename(cls, v: str) -> str:
        """Validates that the filename is not empty or whitespace, and strips leading/trailing spaces."""
        if not v or v.isspace():
            raise ValueError('Filename cannot be empty or whitespace')
        return v.strip()

    @validator('image_width', 'image_height')
    def validate_dimensions(cls, v: Optional[int]) -> Optional[int]:
        """Validates that image dimensions fall within the acceptable range of 0 to 10000."""
        if v is not None and (v < 0 or v > 10000):
            raise ValueError('Image dimensions must be between 0 and 10000')
        return v

    class Config:
        use_enum_values = True
        validate_assignment = True
        arbitrary_types_allowed = False
