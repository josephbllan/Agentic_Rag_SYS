"""
Thread-safe in-memory token blacklist for logout.
Production systems should replace this with Redis or a persistent store.
"""
import threading
from typing import Set


class TokenBlacklist:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls) -> "TokenBlacklist":
        with cls._lock:
            if cls._instance is None:
                inst = super().__new__(cls)
                inst._tokens: Set[str] = set()
                inst._rw_lock = threading.Lock()
                cls._instance = inst
            return cls._instance

    def revoke(self, token: str) -> None:
        with self._rw_lock:
            self._tokens.add(token)

    def is_revoked(self, token: str) -> bool:
        with self._rw_lock:
            return token in self._tokens

    def clear(self) -> None:
        with self._rw_lock:
            self._tokens.clear()


blacklist = TokenBlacklist()
