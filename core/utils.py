"""Lightweight utility functions (no heavy ML imports)."""
import hashlib


def stable_text_hash(text: str) -> str:
    """Deterministic hash for cache keys (unlike built-in hash())"""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
