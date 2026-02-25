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
        """Creates or returns the singleton TokenBlacklist instance,
        using a class-level lock to ensure thread-safe initialization.
        """
        with cls._lock:
            if cls._instance is None:
                inst = super().__new__(cls)
                inst._tokens: Set[str] = set()
                inst._rw_lock = threading.Lock()
                cls._instance = inst
            return cls._instance

    def revoke(self, token: str) -> None:
        """Adds the given token to the blacklist set, marking it
        as revoked so subsequent validation checks will reject it.
        """
        with self._rw_lock:
            self._tokens.add(token)

    def is_revoked(self, token: str) -> bool:
        """Checks whether the given token has been revoked by looking
        it up in the in-memory blacklist set.
        """
        with self._rw_lock:
            return token in self._tokens

    def clear(self) -> None:
        """Removes all tokens from the blacklist, effectively
        restoring all previously revoked tokens.
        """
        with self._rw_lock:
            self._tokens.clear()


blacklist = TokenBlacklist()
