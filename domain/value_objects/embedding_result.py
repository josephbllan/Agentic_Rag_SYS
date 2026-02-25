from dataclasses import dataclass, field
from datetime import datetime, timezone
from ..enums import ModelName
from ..types import VectorType


@dataclass(frozen=True)
class EmbeddingResult:
    vector: VectorType
    dimension: int
    model_name: ModelName
    generated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    processing_time: float = 0.0

    def __post_init__(self):
        """Validates that the vector length matches the declared dimension
        and that the processing time is non-negative.
        """
        if self.dimension != len(self.vector):
            raise ValueError(f"Dimension mismatch: expected {self.dimension}, got {len(self.vector)}")
        if self.processing_time < 0:
            raise ValueError("processing_time must be non-negative")
