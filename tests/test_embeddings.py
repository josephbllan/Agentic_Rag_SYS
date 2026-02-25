"""Tests for the stable_text_hash utility (no heavy ML imports)."""
import pytest
from core.utils import stable_text_hash


class TestStableTextHash:
    def test_deterministic(self):
        assert stable_text_hash("hello") == stable_text_hash("hello")

    def test_different_inputs_differ(self):
        assert stable_text_hash("hello") != stable_text_hash("world")

    def test_returns_hex_string(self):
        h = stable_text_hash("test")
        assert all(c in "0123456789abcdef" for c in h)

    def test_fixed_length(self):
        assert len(stable_text_hash("anything")) == 16
