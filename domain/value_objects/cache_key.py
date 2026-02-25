from dataclasses import dataclass


@dataclass(frozen=True)
class CacheKey:
    key: str
    namespace: str = "default"
    version: int = 1

    def __post_init__(self):
        if not self.key or not self.key.strip():
            raise ValueError("Key cannot be empty")
        if self.version < 1:
            raise ValueError("Version must be positive")

    def to_string(self) -> str:
        return f"{self.namespace}:{self.key}:v{self.version}"
