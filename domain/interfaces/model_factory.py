from typing import Protocol, List, Any, runtime_checkable
from .embedding_model import IEmbeddingModel


@runtime_checkable
class IModelFactory(Protocol):
    def create_model(self, model_type: str, **kwargs: Any) -> IEmbeddingModel:
        """Creates and returns an embedding model instance of the specified type."""
        ...

    def get_supported_models(self) -> List[str]:
        """Returns a list of model type names that this factory can create."""
        ...
