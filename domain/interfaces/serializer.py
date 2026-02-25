from typing import Protocol, Generic, runtime_checkable
from ..types import T


@runtime_checkable
class ISerializer(Protocol, Generic[T]):
    def serialize(self, obj: T) -> str:
        """Serializes the given object into a string representation."""
        ...

    def deserialize(self, data: str) -> T:
        """Deserializes the string data back into an object of type T."""
        ...
