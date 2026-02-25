from typing import Protocol, Dict, Any, Callable, runtime_checkable


@runtime_checkable
class IEventPublisher(Protocol):
    def publish(self, event_type: str, data: Dict[str, Any]) -> None:
        """Publishes an event of the given type with the associated data payload."""
        ...

    def subscribe(self, event_type: str, handler: Callable) -> None:
        """Registers a handler to be called when an event of the given type is published."""
        ...

    def unsubscribe(self, event_type: str, handler: Callable) -> None:
        """Removes a previously registered handler for the given event type."""
        ...
