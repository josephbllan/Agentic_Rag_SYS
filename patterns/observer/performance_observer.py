from typing import List, Dict, Any
import logging
from .base_observer import Observer
from .subject import Subject


class PerformanceEventObserver(Observer):
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._execution_times: List[float] = []
        self._max_samples = 1000

    def update(self, subject: Subject, event_type: str, data: Dict[str, Any]) -> None:
        if event_type == "operation_completed":
            t = data.get("execution_time", 0.0)
            self._execution_times.append(t)
            if len(self._execution_times) > self._max_samples:
                self._execution_times.pop(0)
            if t > 5.0:
                self._logger.warning(f"Slow: {data.get('operation', '')} took {t:.2f}s")

    @property
    def avg_execution_time(self) -> float:
        return sum(self._execution_times) / len(self._execution_times) if self._execution_times else 0.0

    @property
    def stats(self) -> Dict[str, Any]:
        if not self._execution_times:
            return {"count": 0, "avg": 0.0, "min": 0.0, "max": 0.0}
        return {"count": len(self._execution_times), "avg": self.avg_execution_time, "min": min(self._execution_times), "max": max(self._execution_times)}
