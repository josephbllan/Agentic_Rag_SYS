from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True)
class VectorIdentifier:
    id: str
    collection: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self):
        if not self.id or not self.id.strip():
            raise ValueError("ID cannot be empty")
        if not self.collection or not self.collection.strip():
            raise ValueError("Collection cannot be empty")

    def to_string(self) -> str:
        return f"{self.collection}:{self.id}"
