from abc import ABC, abstractmethod
from typing import Generic, List
import logging
from ..types import T


class BaseValidator(ABC, Generic[T]):
    def __init__(self, validator_name: str):
        self._validator_name = validator_name
        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def validator_name(self) -> str:
        return self._validator_name

    @abstractmethod
    def validate(self, data: T) -> tuple[bool, List[str]]:
        pass

    def is_valid(self, data: T) -> bool:
        valid, _ = self.validate(data)
        return valid

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self._validator_name}')"
