"""Tests for core.search_engine.SearchEngine (using injected FakeVectorDB).

Heavy ML imports (clip, sentence_transformers, torch) are mocked out so
these tests run in seconds without GPU/model downloads.
"""
import sys
from unittest.mock import MagicMock

# Mock heavy ML modules before any project import touches them
for mod_name in [
    "clip", "sentence_transformers", "torch", "torchvision",
    "torchvision.transforms", "torchvision.models",
]:
    if mod_name not in sys.modules:
        sys.modules[mod_name] = MagicMock()

import numpy as np
import pytest
from unittest.mock import patch

from core.search_engine import SearchEngine


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_embedding_manager():
    mgr = MagicMock()
    mgr.get_text_embedding.return_value = np.random.rand(512).astype("float32")
    mgr.get_image_embedding.return_value = np.random.rand(512).astype("float32")
    return mgr


@pytest.fixture
def seeded_db(fake_vector_db, random_vectors):
    metadata = [
        {"filename": f"shoe_{i}.jpg", "brand": "nike" if i % 2 == 0 else "adidas"}
        for i in range(5)
    ]
    fake_vector_db.add_vectors(random_vectors, metadata)
    return fake_vector_db


@pytest.fixture
def engine(seeded_db, mock_embedding_manager):
    return SearchEngine(
        vector_db=seeded_db,
        embedding_manager=mock_embedding_manager,
        multimodal_embedder=MagicMock(),
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestHybridScoring:
    def test_single_score_returns_itself(self, engine):
        assert engine._hybrid_score({"text": 0.9}) == pytest.approx(0.9, abs=0.01)

    def test_all_zeros_returns_zero(self, engine):
        assert engine._hybrid_score({}) == 0.0

    def test_weighted_average(self, engine):
        scores = {"visual": 0.8, "text": 0.6, "metadata": 1.0}
        result = engine._hybrid_score(scores)
        expected = (0.8 * 0.4 + 0.6 * 0.3 + 1.0 * 0.3) / (0.4 + 0.3 + 0.3)
        assert result == pytest.approx(expected, abs=0.001)


class TestTextSearch:
    @patch("core.search_analytics.get_db_session")
    def test_returns_results(self, mock_db, engine):
        mock_db.return_value.__enter__ = MagicMock()
        mock_db.return_value.__exit__ = MagicMock(return_value=False)
        results = engine.text_to_image_search("red shoes", limit=3)
        assert isinstance(results, list)

    @patch("core.search_analytics.get_db_session")
    def test_respects_limit(self, mock_db, engine):
        mock_db.return_value.__enter__ = MagicMock()
        mock_db.return_value.__exit__ = MagicMock(return_value=False)
        results = engine.text_to_image_search("shoes", limit=2)
        assert len(results) <= 2


class TestQueryExpansion:
    def test_includes_original(self, engine):
        expanded = engine._expand_query("blue shoe")
        assert "blue shoe" in expanded

    def test_expands_shoe(self, engine):
        expanded = engine._expand_query("red shoe")
        assert any("sneaker" in q for q in expanded)

    def test_expands_nike(self, engine):
        expanded = engine._expand_query("nike shoes")
        assert any("nike air" in q for q in expanded)


class TestDIInjection:
    def test_accepts_custom_vector_db(self, fake_vector_db):
        engine = SearchEngine(
            vector_db=fake_vector_db,
            embedding_manager=MagicMock(),
            multimodal_embedder=MagicMock(),
        )
        assert engine.vector_db is fake_vector_db
