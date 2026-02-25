from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class SearchScore:
    visual_score: float = 0.0
    text_score: float = 0.0
    metadata_score: float = 0.0
    hybrid_score: float = 0.0

    def __post_init__(self):
        """Validates that all score components are between 0.0 and 1.0."""
        for s in [self.visual_score, self.text_score, self.metadata_score, self.hybrid_score]:
            if not 0.0 <= s <= 1.0:
                raise ValueError("All scores must be between 0 and 1")

    def to_dict(self) -> Dict[str, float]:
        """Converts the search scores into a dictionary keyed by score type."""
        return {"visual": self.visual_score, "text": self.text_score, "metadata": self.metadata_score, "hybrid": self.hybrid_score}
