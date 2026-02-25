from typing import Protocol, List, Any, runtime_checkable
from ..types import VectorType


@runtime_checkable
class IEmbeddingModel(Protocol):
    @property
    def dimension(self) -> int:
        """Returns the dimensionality of the vectors produced by this model."""
        ...

    @property
    def model_name(self) -> str:
        """Returns the name of the embedding model."""
        ...

    def encode(self, input_data: Any) -> VectorType:
        """Encodes the given input data into a vector representation."""
        ...

    def encode_batch(self, inputs: List[Any], batch_size: int = 32) -> List[VectorType]:
        """Encodes a list of inputs in batches and returns the resulting vectors."""
        ...
