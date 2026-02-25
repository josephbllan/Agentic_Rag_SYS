from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass(frozen=True)
class ModelVersion:
    name: str
    version: str
    checksum: Optional[str] = None
    loaded_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self):
        """Validates that both the model name and version string are non-empty."""
        if not self.name or not self.name.strip():
            raise ValueError("Model name cannot be empty")
        if not self.version or not self.version.strip():
            raise ValueError("Version cannot be empty")
