from typing import Protocol, Generic, List, runtime_checkable
from ..types import T


@runtime_checkable
class IValidator(Protocol, Generic[T]):
    def validate(self, data: T) -> tuple[bool, List[str]]:
        """Validates the given data and returns a tuple of (is_valid, error_messages)."""
        ...

    def is_valid(self, data: T) -> bool:
        """Returns True if the data passes all validation rules, False otherwise."""
        ...
