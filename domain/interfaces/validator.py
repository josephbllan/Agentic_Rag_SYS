from typing import Protocol, Generic, List, runtime_checkable
from ..types import T


@runtime_checkable
class IValidator(Protocol, Generic[T]):
    def validate(self, data: T) -> tuple[bool, List[str]]: ...
    def is_valid(self, data: T) -> bool: ...
