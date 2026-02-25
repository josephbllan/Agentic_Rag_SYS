from abc import ABC, abstractmethod
from typing import Any


class AbstractFactory(ABC):
    @abstractmethod
    def create(self, *args, **kwargs) -> Any:
        """Creates and returns a new product instance.
        Subclasses must provide a concrete implementation.
        """
        pass
