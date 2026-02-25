from typing import List, Dict, Any
from pydantic import BaseModel, Field, validator


class IndexingResult(BaseModel):
    total_processed: int = Field(0, ge=0)
    successful: int = Field(0, ge=0)
    failed: int = Field(0, ge=0)
    execution_time: float = Field(0.0, ge=0.0)
    errors: List[str] = Field(default_factory=list)

    @validator('successful', 'failed')
    def validate_counts(cls, v: int, values: Dict[str, Any]) -> int:
        if 'total_processed' in values:
            if v > values['total_processed']:
                raise ValueError('Count cannot exceed total processed')
        return v

    class Config:
        validate_assignment = True
