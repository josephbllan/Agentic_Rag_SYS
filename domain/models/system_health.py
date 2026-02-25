from typing import List
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class SystemHealth(BaseModel):
    status: str = "healthy"
    vector_db_status: str = "connected"
    models_loaded: List[str] = Field(default_factory=list)
    total_vectors: int = Field(0, ge=0)
    uptime_seconds: float = Field(0.0, ge=0.0)
    last_check: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        use_enum_values = True
