"""Tests for the FakeVectorDB (validates the interface contract)
and for the BaseVectorDB._apply_filters helper."""
import numpy as np
import pytest

from core.vector_db import BaseVectorDB


class TestApplyFilters:
    """Test the static _apply_filters helper shared by all backends."""

    def test_no_filters_returns_all(self):
        """Verifies that an empty filter dict returns all input records."""
        data = [{"brand": "nike"}, {"brand": "adidas"}]
        assert BaseVectorDB._apply_filters(data, {}) == data

    def test_single_filter(self):
        """Checks that a single key-value filter correctly narrows results."""
        data = [
            {"brand": "nike", "size": "large"},
            {"brand": "adidas", "size": "small"},
        ]
        filtered = BaseVectorDB._apply_filters(data, {"brand": "nike"})
        assert len(filtered) == 1
        assert filtered[0]["brand"] == "nike"

    def test_list_filter(self):
        """Verifies that a list-valued filter matches any of the listed values."""
        data = [
            {"brand": "nike"},
            {"brand": "puma"},
            {"brand": "adidas"},
        ]
        filtered = BaseVectorDB._apply_filters(data, {"brand": ["nike", "adidas"]})
        assert len(filtered) == 2

    def test_missing_key_excluded(self):
        """Confirms that records lacking the filter key are excluded from results."""
        data = [{"brand": "nike"}]
        filtered = BaseVectorDB._apply_filters(data, {"color": "red"})
        assert len(filtered) == 0


class TestFakeVectorDB:
    """Integration-style tests using conftest.FakeVectorDB."""

    def test_add_and_search(self, fake_vector_db, random_vectors):
        """Tests that vectors can be added and then retrieved via similarity search."""
        meta = [{"filename": f"f{i}.jpg"} for i in range(5)]
        fake_vector_db.add_vectors(random_vectors, meta)
        query = random_vectors[0]
        results = fake_vector_db.search(query, k=3)
        assert len(results) <= 3
        assert results[0]["similarity_score"] > 0

    def test_delete_vector(self, fake_vector_db):
        """Verifies that deleting a vector removes it from the store entirely."""
        vec = np.random.rand(1, 512).astype("float32")
        fake_vector_db.add_vectors(vec, [{"filename": "a.jpg"}], ids=["id1"])
        fake_vector_db.delete_vector("id1")
        assert fake_vector_db.get_stats()["total_vectors"] == 0

    def test_stats(self, fake_vector_db, random_vectors):
        """Checks that get_stats reports the correct total vector count after insertion."""
        meta = [{"filename": f"f{i}.jpg"} for i in range(5)]
        fake_vector_db.add_vectors(random_vectors, meta)
        stats = fake_vector_db.get_stats()
        assert stats["total_vectors"] == 5
