from typing import Protocol, Dict, runtime_checkable
from ..types import VectorType


@runtime_checkable
class IScorer(Protocol):
    def calculate_score(self, query_vector: VectorType, result_vector: VectorType) -> float:
        """Calculates the similarity score between a query vector and a result vector."""
        ...

    def calculate_hybrid_score(self, scores: Dict[str, float]) -> float:
        """Computes a combined score from multiple named score components."""
        ...
