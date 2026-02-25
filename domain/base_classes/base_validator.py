from abc import ABC, abstractmethod
from typing import Generic, List
import logging
from ..types import T


class BaseValidator(ABC, Generic[T]):
    def __init__(self, validator_name: str):
        """Initializes the validator with the given name and sets up logging."""
        self._validator_name = validator_name
        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def validator_name(self) -> str:
        """Returns the name of this validator."""
        return self._validator_name

    @abstractmethod
    def validate(self, data: T) -> tuple[bool, List[str]]:
        """Validates the given data and returns a tuple of (is_valid, error_messages).
        Subclasses must implement the specific validation rules.
        """
        pass

    def is_valid(self, data: T) -> bool:
        """Returns True if the data passes validation, False otherwise."""
        valid, _ = self.validate(data)
        return valid

    def __repr__(self) -> str:
        """Returns a string representation including the validator name."""
        return f"{self.__class__.__name__}(name='{self._validator_name}')"
