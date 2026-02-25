from abc import ABC, abstractmethod
from typing import Any


class AbstractFactory(ABC):
    @abstractmethod
    def create(self, *args, **kwargs) -> Any:
        pass
