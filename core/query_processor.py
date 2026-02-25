"""Natural Language Query Processing for RAG System."""
import re
from typing import Dict, List, Any, Optional, Tuple
import logging

from config.settings import METADATA_CATEGORIES
from core.query_data import (
    QueryIntent,
    PATTERNS,
    SYNONYMS,
    BRAND_ALIASES,
    extract_image_path,
    extract_similarity_threshold,
    extract_limit,
    validate_query,
)

logger = logging.getLogger(__name__)


class QueryProcessor:
    """Process natural language queries and extract search parameters."""

    def __init__(self):
        """Initializes the query processor with predefined regex patterns,
        synonym mappings, and brand alias lookups."""
        self.patterns = PATTERNS
        self.synonyms = SYNONYMS
        self.brand_aliases = BRAND_ALIASES

    def process_query(self, query: str) -> QueryIntent:
        """Processes a raw natural language query into a structured QueryIntent
        containing search terms, filters, and query type."""
        try:
            normalized = self._normalize_query(query)
            search_terms = self._extract_search_terms(normalized)
            filters = self._extract_filters(normalized)
            query_type = self._determine_query_type(normalized, filters)
            return QueryIntent(
                query_type=query_type,
                search_terms=search_terms,
                filters=filters,
                image_path=extract_image_path(normalized),
                similarity_threshold=extract_similarity_threshold(normalized),
                limit=extract_limit(normalized),
            )
        except Exception as e:
            logger.error(f"Query processing failed: {e}")
            return QueryIntent(query_type="text", search_terms=[query], filters={})

    def _normalize_query(self, query: str) -> str:
        """Lowercases the query, collapses whitespace, and expands
        common English contractions."""
        normalized = query.lower()
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        contractions = {
            "don't": "do not", "won't": "will not", "can't": "cannot",
            "n't": " not", "'re": " are", "'s": " is",
            "'ve": " have", "'ll": " will",
        }
        for contraction, expansion in contractions.items():
            normalized = normalized.replace(contraction, expansion)
        return normalized

    def _extract_search_terms(self, query: str) -> List[str]:
        """Extracts meaningful search terms from the query by removing
        stop words and expanding synonyms."""
        filter_words = {
            "with", "that", "have", "are", "is", "in", "of", "for",
            "and", "or", "the", "a", "an", "this", "these", "those",
            "my", "your", "his", "her",
        }
        terms: List[str] = []
        for word in query.split():
            if word not in filter_words and len(word) > 2:
                terms.extend(self._expand_term(word))
        return list(set(terms))

    def _extract_filters(self, query: str) -> Dict[str, Any]:
        """Extracts structured metadata filters (brand, pattern, shape,
        size, color, style) from the normalized query text."""
        filters: Dict[str, Any] = {}
        brand = self._match_patterns(query, self.patterns["brand"])
        if brand:
            brand = self._normalize_brand(brand)
            if brand in METADATA_CATEGORIES["brands"]:
                filters["brand"] = brand
        pattern = self._match_patterns(query, self.patterns["pattern"])
        if pattern and pattern.lower() in METADATA_CATEGORIES["patterns"]:
            filters["pattern"] = pattern.lower()
        shape = self._match_patterns(query, self.patterns["shape"])
        if shape and shape.lower() in METADATA_CATEGORIES["shapes"]:
            filters["shape"] = shape.lower()
        size = self._match_patterns(query, self.patterns["size"])
        if size:
            size = self._normalize_size(size)
            if size in METADATA_CATEGORIES["sizes"]:
                filters["size"] = size
        color = self._match_patterns(query, self.patterns["color"])
        if color:
            filters["color"] = color.lower()
        style = self._match_patterns(query, self.patterns["style"])
        if style:
            filters["style"] = style.lower()
        return filters

    def _match_patterns(self, query: str, patterns: List[str]) -> Optional[str]:
        """Tries each regex pattern against the query and returns the first
        captured group from the first match, or None."""
        for pattern in patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                return match.group(1)
        return None

    def _normalize_brand(self, brand: str) -> str:
        """Resolves brand aliases to their canonical name, falling back
        to 'other' if the brand is not recognized."""
        brand = brand.lower()
        for alias, canonical in self.brand_aliases.items():
            if alias in brand:
                return canonical
        if brand in METADATA_CATEGORIES["brands"]:
            return brand
        return "other"

    def _normalize_size(self, size: str) -> str:
        """Normalizes size strings such as 'xl' or 'extra large' to their
        canonical metadata category values."""
        size = size.lower()
        if size in ("xl", "extra large", "extra-large"):
            return "extra_large"
        return size if size in METADATA_CATEGORIES["sizes"] else "medium"

    def _expand_term(self, term: str) -> List[str]:
        """Expands a single search term into a list that includes its
        synonyms or the canonical form it maps to."""
        expanded = [term]
        for canonical, syns in self.synonyms.items():
            if term in syns:
                expanded.append(canonical)
            elif term == canonical:
                expanded.extend(syns)
        return expanded

    def _determine_query_type(self, query: str, filters: Dict[str, Any]) -> str:
        """Classifies the query as text, image, metadata, or hybrid based
        on keyword cues and the number of extracted filters."""
        if any(kw in query for kw in ("similar to", "like this", "matching", "comparable")):
            return "image"
        if not any(w in query for w in ("find", "show", "search", "get", "look for")):
            if filters:
                return "metadata"
        if len(filters) > 2 or any(w in query for w in ("and", "with", "that have")):
            return "hybrid"
        return "text"

    def generate_query_variations(self, query: str) -> List[str]:
        """Generates alternative phrasings of a query by substituting
        synonyms and prepending action verbs."""
        variations = [query]
        words = query.split()
        for i, word in enumerate(words):
            for canonical, syns in self.synonyms.items():
                if word in syns:
                    for syn in syns:
                        if syn != word:
                            new = words.copy()
                            new[i] = syn
                            variations.append(" ".join(new))
        if not query.endswith("?"):
            variations.append(query + "?")
        if not query.startswith(("find", "show", "search", "get")):
            variations.extend([f"find {query}", f"show me {query}"])
        return list(set(variations))

    def validate_query(self, query: str) -> Tuple[bool, str]:
        """Delegates query validation to the stateless validator and returns
        a tuple of validity flag and status message."""
        return validate_query(query)


def create_query_processor() -> QueryProcessor:
    """Creates and returns a new QueryProcessor instance."""
    return QueryProcessor()


def process_natural_query(query: str) -> QueryIntent:
    """Convenience function that creates a processor and processes the
    given query in a single call."""
    return create_query_processor().process_query(query)
