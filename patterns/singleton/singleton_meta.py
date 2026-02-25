from typing import Dict, Any
from threading import Lock


class SingletonMeta(type):
    _instances: Dict[type, Any] = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        """Controls instance creation to ensure only one instance exists per class.
        Uses double-checked locking for thread safety.
        """
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
