from abc import ABC, abstractmethod
from typing import List, Any
import logging
from ..types import VectorType


class BaseEmbeddingModel(ABC):
    def __init__(self, model_name: str, device: str = "cpu"):
        """Initializes the embedding model with the given name and target device.
        Sets up logging and default state for lazy model loading.
        """
        self._model_name = model_name
        self._device = device
        self._dimension: int = 0
        self._model: Any = None
        self._logger = logging.getLogger(self.__class__.__name__)
        self._is_loaded = False

    @property
    def model_name(self) -> str:
        """Returns the name of the underlying embedding model."""
        return self._model_name

    @property
    def device(self) -> str:
        """Returns the device (e.g., 'cpu' or 'cuda') on which the model runs."""
        return self._device

    @property
    def dimension(self) -> int:
        """Returns the dimensionality of the vectors produced by this model."""
        return self._dimension

    @property
    def is_loaded(self) -> bool:
        """Indicates whether the model has been loaded into memory."""
        return self._is_loaded

    @abstractmethod
    def _load_model(self) -> None:
        """Loads the embedding model into memory.
        Subclasses must implement the specific model loading logic.
        """
        pass

    @abstractmethod
    def encode(self, input_data: Any) -> VectorType:
        """Encodes the given input data into a vector representation.
        Subclasses must implement the encoding logic for their specific model.
        """
        pass

    def encode_batch(self, inputs: List[Any], batch_size: int = 32) -> List[VectorType]:
        """Encodes a list of inputs in batches and returns the resulting vectors.
        Iterates through the inputs in chunks of the specified batch size.
        """
        results = []
        for i in range(0, len(inputs), batch_size):
            batch = inputs[i:i + batch_size]
            self._logger.debug(f"Encoding batch {i // batch_size + 1}")
            batch_results = [self.encode(item) for item in batch]
            results.extend(batch_results)
        return results

    def warmup(self) -> None:
        """Warms up the model by running a dummy encoding pass.
        Logs a warning if the warmup fails without raising an exception.
        """
        try:
            self._logger.info("Warming up model...")
            dummy_input = self._get_dummy_input()
            self.encode(dummy_input)
            self._logger.info("Model warmup completed")
        except Exception as e:
            self._logger.warning(f"Model warmup failed: {e}")

    @abstractmethod
    def _get_dummy_input(self) -> Any:
        """Returns a dummy input suitable for warming up the model.
        Subclasses must provide an input matching their expected data format.
        """
        pass

    def __repr__(self) -> str:
        """Returns a string representation including the model name and device."""
        return f"{self.__class__.__name__}(model_name='{self._model_name}', device='{self._device}')"
