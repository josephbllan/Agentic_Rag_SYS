from typing import Dict, Any
import logging
from .base_observer import Observer
from .subject import Subject


class CacheEventObserver(Observer):
    def __init__(self):
        """Initializes the cache event observer with hit and miss counters set to zero."""
        self._logger = logging.getLogger(self.__class__.__name__)
        self._hits = 0
        self._misses = 0

    def update(self, subject: Subject, event_type: str, data: Dict[str, Any]) -> None:
        """Processes cache-related events and updates hit/miss statistics accordingly.
        Resets counters when a cache_cleared event is received.
        """
        if event_type == "cache_hit":
            self._hits += 1
        elif event_type == "cache_miss":
            self._misses += 1
        elif event_type == "cache_cleared":
            self._hits = self._misses = 0

    @property
    def hit_rate(self) -> float:
        """Calculates and returns the cache hit rate as a ratio of hits to total requests."""
        total = self._hits + self._misses
        return self._hits / total if total > 0 else 0.0

    @property
    def stats(self) -> Dict[str, Any]:
        """Returns a dictionary containing cache hit, miss, and hit rate statistics."""
        return {"hits": self._hits, "misses": self._misses, "hit_rate": self.hit_rate}
