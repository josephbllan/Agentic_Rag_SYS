from typing import List, Dict, Any, Callable, Optional
from datetime import datetime, timezone
from .subject import Subject


class EventPublisher(Subject):
    def __init__(self):
        """Initializes the event publisher with an empty handler registry and event history."""
        super().__init__()
        self._event_handlers: Dict[str, List[Callable]] = {}
        self._event_history: List[Dict[str, Any]] = []
        self._max_history = 1000

    def subscribe(self, event_type: str, handler: Callable) -> None:
        """Registers an event handler callback for the specified event type.
        Prevents duplicate registrations of the same handler.
        """
        self._event_handlers.setdefault(event_type, [])
        if handler not in self._event_handlers[event_type]:
            self._event_handlers[event_type].append(handler)

    def unsubscribe(self, event_type: str, handler: Callable) -> None:
        """Removes an event handler callback from the specified event type."""
        if event_type in self._event_handlers and handler in self._event_handlers[event_type]:
            self._event_handlers[event_type].remove(handler)

    def publish(self, event_type: str, data: Dict[str, Any]) -> None:
        """Publishes an event by recording it in history, invoking registered handlers,
        and notifying attached observers.
        """
        event = {"type": event_type, "data": data, "timestamp": datetime.now(timezone.utc)}
        self._event_history.append(event)
        if len(self._event_history) > self._max_history:
            self._event_history.pop(0)
        if event_type in self._event_handlers:
            for handler in self._event_handlers[event_type]:
                try:
                    handler(data)
                except Exception as e:
                    self._logger.error(f"Error in event handler: {e}")
        self.notify(event_type, data)

    def get_event_history(self, event_type: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieves the event history, optionally filtered by event type and limited in count."""
        if event_type:
            return [e for e in self._event_history if e["type"] == event_type][-limit:]
        return self._event_history[-limit:]

    def clear_history(self) -> None:
        """Clears the entire event history log."""
        self._event_history.clear()
