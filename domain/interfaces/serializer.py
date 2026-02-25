from typing import Protocol, Generic, runtime_checkable
from ..types import T


@runtime_checkable
class ISerializer(Protocol, Generic[T]):
    def serialize(self, obj: T) -> str: ...
    def deserialize(self, data: str) -> T: ...
