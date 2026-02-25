"""Tests for core.query_processor.QueryProcessor"""
import pytest
from core.query_processor import QueryProcessor, QueryIntent
from core.query_data import extract_limit


@pytest.fixture
def qp():
    return QueryProcessor()


# ----- normalisation ---------------------------------------------------

class TestNormalize:
    def test_lowercases_and_strips(self, qp):
        assert qp._normalize_query("  HELLO  WORLD  ") == "hello world"

    def test_expands_contractions(self, qp):
        result = qp._normalize_query("don't won't can't")
        assert "do not" in result
        assert "will not" in result
        assert "cannot" in result


# ----- filter extraction ------------------------------------------------

class TestFilterExtraction:
    def test_extracts_brand(self, qp):
        intent = qp.process_query("Find Nike shoes")
        assert intent.filters.get("brand") == "nike"

    def test_extracts_pattern(self, qp):
        intent = qp.process_query("Show zigzag pattern shoes")
        assert intent.filters.get("pattern") == "zigzag"

    def test_extracts_shape(self, qp):
        intent = qp.process_query("round shaped sneakers")
        assert intent.filters.get("shape") == "round"

    def test_extracts_size(self, qp):
        intent = qp.process_query("large sized shoe")
        assert intent.filters.get("size") == "large"

    def test_no_false_brand_on_generic_query(self, qp):
        intent = qp.process_query("comfortable everyday footwear")
        assert intent.filters.get("brand") is None or intent.filters.get("brand") == "other"


# ----- query type determination -----------------------------------------

class TestQueryType:
    def test_image_query_detected(self, qp):
        intent = qp.process_query("Find shoes similar to this image: test.jpg")
        assert intent.query_type == "image"

    def test_text_query_default(self, qp):
        intent = qp.process_query("Find blue running shoes")
        assert intent.query_type in ("text", "hybrid")


# ----- limit extraction -------------------------------------------------

class TestLimitExtraction:
    def test_extracts_numeric_limit(self):
        assert extract_limit("show me 20 results") == 20

    def test_extracts_word_limit(self):
        assert extract_limit("show me five shoes") == 5

    def test_default_limit(self):
        assert extract_limit("some query") == 10


# ----- validation -------------------------------------------------------

class TestValidation:
    def test_valid_query(self, qp):
        ok, msg = qp.validate_query("red nike shoes")
        assert ok is True

    def test_too_short(self, qp):
        ok, _ = qp.validate_query("a")
        assert ok is False

    def test_too_long(self, qp):
        ok, _ = qp.validate_query("x" * 501)
        assert ok is False

    def test_rejects_script_injection(self, qp):
        ok, _ = qp.validate_query("<script>alert(1)</script>")
        assert ok is False


# ----- query variations -------------------------------------------------

class TestQueryVariations:
    def test_returns_at_least_original(self, qp):
        variations = qp.generate_query_variations("red shoe")
        assert "red shoe" in variations

    def test_adds_command_prefix(self, qp):
        variations = qp.generate_query_variations("red shoe")
        assert any(v.startswith("find") for v in variations)
