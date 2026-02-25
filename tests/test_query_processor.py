"""Tests for core.query_processor.QueryProcessor"""
import pytest
from core.query_processor import QueryProcessor, QueryIntent
from core.query_data import extract_limit


@pytest.fixture
def qp():
    """Provides a fresh QueryProcessor instance for each test."""
    return QueryProcessor()


# ----- normalisation ---------------------------------------------------

class TestNormalize:
    def test_lowercases_and_strips(self, qp):
        """Verifies that normalization lowercases text and collapses whitespace."""
        assert qp._normalize_query("  HELLO  WORLD  ") == "hello world"

    def test_expands_contractions(self, qp):
        """Checks that common English contractions are expanded during normalization."""
        result = qp._normalize_query("don't won't can't")
        assert "do not" in result
        assert "will not" in result
        assert "cannot" in result


# ----- filter extraction ------------------------------------------------

class TestFilterExtraction:
    def test_extracts_brand(self, qp):
        """Verifies that a brand name is correctly extracted from the query."""
        intent = qp.process_query("Find Nike shoes")
        assert intent.filters.get("brand") == "nike"

    def test_extracts_pattern(self, qp):
        """Verifies that a pattern filter is correctly extracted from the query."""
        intent = qp.process_query("Show zigzag pattern shoes")
        assert intent.filters.get("pattern") == "zigzag"

    def test_extracts_shape(self, qp):
        """Verifies that a shape filter is correctly extracted from the query."""
        intent = qp.process_query("round shaped sneakers")
        assert intent.filters.get("shape") == "round"

    def test_extracts_size(self, qp):
        """Verifies that a size filter is correctly extracted from the query."""
        intent = qp.process_query("large sized shoe")
        assert intent.filters.get("size") == "large"

    def test_no_false_brand_on_generic_query(self, qp):
        """Ensures that a generic query does not produce a spurious brand filter."""
        intent = qp.process_query("comfortable everyday footwear")
        assert intent.filters.get("brand") is None or intent.filters.get("brand") == "other"


# ----- query type determination -----------------------------------------

class TestQueryType:
    def test_image_query_detected(self, qp):
        """Checks that a query referencing an image file is classified as image type."""
        intent = qp.process_query("Find shoes similar to this image: test.jpg")
        assert intent.query_type == "image"

    def test_text_query_default(self, qp):
        """Verifies that a plain text query defaults to text or hybrid type."""
        intent = qp.process_query("Find blue running shoes")
        assert intent.query_type in ("text", "hybrid")


# ----- limit extraction -------------------------------------------------

class TestLimitExtraction:
    def test_extracts_numeric_limit(self):
        """Checks that a numeric limit embedded in the query string is parsed correctly."""
        assert extract_limit("show me 20 results") == 20

    def test_extracts_word_limit(self):
        """Checks that a spelled-out number word is converted to the correct limit."""
        assert extract_limit("show me five shoes") == 5

    def test_default_limit(self):
        """Verifies that queries without an explicit limit default to 10."""
        assert extract_limit("some query") == 10


# ----- validation -------------------------------------------------------

class TestValidation:
    def test_valid_query(self, qp):
        """Confirms that a well-formed query passes validation."""
        ok, msg = qp.validate_query("red nike shoes")
        assert ok is True

    def test_too_short(self, qp):
        """Confirms that a single-character query fails validation."""
        ok, _ = qp.validate_query("a")
        assert ok is False

    def test_too_long(self, qp):
        """Confirms that a query exceeding 500 characters fails validation."""
        ok, _ = qp.validate_query("x" * 501)
        assert ok is False

    def test_rejects_script_injection(self, qp):
        """Ensures that queries containing script tags are rejected."""
        ok, _ = qp.validate_query("<script>alert(1)</script>")
        assert ok is False


# ----- query variations -------------------------------------------------

class TestQueryVariations:
    def test_returns_at_least_original(self, qp):
        """Checks that generated variations always include the original query."""
        variations = qp.generate_query_variations("red shoe")
        assert "red shoe" in variations

    def test_adds_command_prefix(self, qp):
        """Verifies that at least one variation includes a 'find' prefix."""
        variations = qp.generate_query_variations("red shoe")
        assert any(v.startswith("find") for v in variations)
