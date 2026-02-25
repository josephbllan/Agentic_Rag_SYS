from typing import Protocol, Dict, runtime_checkable
from ..types import VectorType


@runtime_checkable
class IScorer(Protocol):
    def calculate_score(self, query_vector: VectorType, result_vector: VectorType) -> float: ...
    def calculate_hybrid_score(self, scores: Dict[str, float]) -> float: ...
