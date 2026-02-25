from typing import Protocol, List, Any, runtime_checkable
from .embedding_model import IEmbeddingModel


@runtime_checkable
class IModelFactory(Protocol):
    def create_model(self, model_type: str, **kwargs: Any) -> IEmbeddingModel: ...
    def get_supported_models(self) -> List[str]: ...
