from typing import Dict, Type
import logging
from domain.base_classes import BaseEmbeddingModel


class ModelFactory:
    _model_classes: Dict[str, Type[BaseEmbeddingModel]] = {}
    _logger = logging.getLogger("ModelFactory")

    @classmethod
    def register_model(cls, model_type: str, model_class: Type[BaseEmbeddingModel]) -> None:
        cls._model_classes[model_type] = model_class

    @classmethod
    def create_model(cls, model_type: str, model_name: str, device: str = "cpu", **kwargs) -> BaseEmbeddingModel:
        if model_type not in cls._model_classes:
            raise ValueError(f"Unknown model: {model_type}. Available: {list(cls._model_classes.keys())}")
        return cls._model_classes[model_type](model_name=model_name, device=device, **kwargs)

    @classmethod
    def get_supported_models(cls) -> list[str]:
        return list(cls._model_classes.keys())

    @classmethod
    def create_clip_model(cls, model_name: str = "ViT-B/32", device: str = "cpu") -> BaseEmbeddingModel:
        return cls.create_model("clip", model_name, device)

    @classmethod
    def create_resnet_model(cls, model_name: str = "resnet50", device: str = "cpu") -> BaseEmbeddingModel:
        return cls.create_model("resnet", model_name, device)

    @classmethod
    def create_sentence_transformer(cls, model_name: str = "all-MiniLM-L6-v2", device: str = "cpu") -> BaseEmbeddingModel:
        return cls.create_model("sentence_transformer", model_name, device)
