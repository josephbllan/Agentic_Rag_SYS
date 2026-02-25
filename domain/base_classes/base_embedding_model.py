from abc import ABC, abstractmethod
from typing import List, Any
import logging
from ..types import VectorType


class BaseEmbeddingModel(ABC):
    def __init__(self, model_name: str, device: str = "cpu"):
        self._model_name = model_name
        self._device = device
        self._dimension: int = 0
        self._model: Any = None
        self._logger = logging.getLogger(self.__class__.__name__)
        self._is_loaded = False

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def device(self) -> str:
        return self._device

    @property
    def dimension(self) -> int:
        return self._dimension

    @property
    def is_loaded(self) -> bool:
        return self._is_loaded

    @abstractmethod
    def _load_model(self) -> None:
        pass

    @abstractmethod
    def encode(self, input_data: Any) -> VectorType:
        pass

    def encode_batch(self, inputs: List[Any], batch_size: int = 32) -> List[VectorType]:
        results = []
        for i in range(0, len(inputs), batch_size):
            batch = inputs[i:i + batch_size]
            self._logger.debug(f"Encoding batch {i // batch_size + 1}")
            batch_results = [self.encode(item) for item in batch]
            results.extend(batch_results)
        return results

    def warmup(self) -> None:
        try:
            self._logger.info("Warming up model...")
            dummy_input = self._get_dummy_input()
            self.encode(dummy_input)
            self._logger.info("Model warmup completed")
        except Exception as e:
            self._logger.warning(f"Model warmup failed: {e}")

    @abstractmethod
    def _get_dummy_input(self) -> Any:
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(model_name='{self._model_name}', device='{self._device}')"
