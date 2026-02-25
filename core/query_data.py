"""Query data constants, dataclass, and stateless helper functions."""
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class QueryIntent:
    """Represents the parsed intent of a search query."""
    query_type: str  # text, image, hybrid, metadata
    search_terms: List[str]
    filters: Dict[str, Any]
    image_path: Optional[str] = None
    similarity_threshold: float = 0.7
    limit: int = 10


PATTERNS: Dict[str, List[str]] = {
    "brand": [
        r"(nike|adidas|puma|converse|vans|reebok|new balance|asics|under armour|jordan)",
        r"(\w+)\s+(shoes?|sneakers?|footwear)",
    ],
    "pattern": [
        r"(zigzag|circular|square|diamond|brand logo|logo)",
        r"(pattern|design|tread)\s+(zigzag|circular|square|diamond|logo)",
    ],
    "shape": [
        r"(round|square|oval|irregular|elongated)",
        r"(shape|outline)\s+(round|square|oval|irregular|elongated)",
    ],
    "size": [
        r"(small|medium|large|extra large|xl)",
        r"size\s+(small|medium|large|extra large|xl)",
    ],
    "color": [
        r"(red|blue|green|yellow|black|white|gray|grey|brown|pink|purple|orange)",
        r"color\s+(red|blue|green|yellow|black|white|gray|grey|brown|pink|purple|orange)",
    ],
    "style": [
        r"(athletic|running|basketball|tennis|casual|dress|formal|sport)",
        r"(sneakers?|shoes?|boots?|sandals?|flip flops?)",
    ],
    "activity": [
        r"(running|basketball|tennis|walking|hiking|gym|workout|sport)",
        r"for\s+(running|basketball|tennis|walking|hiking|gym|workout|sport)",
    ],
}

SYNONYMS: Dict[str, List[str]] = {
    "shoe": ["shoes", "sneaker", "sneakers", "footwear", "footgear"],
    "red": ["crimson", "scarlet", "burgundy", "maroon"],
    "blue": ["navy", "azure", "cobalt", "royal"],
    "black": ["ebony", "charcoal", "jet"],
    "white": ["ivory", "cream", "pearl"],
    "large": ["big", "huge", "oversized"],
    "small": ["tiny", "mini", "petite"],
    "round": ["circular", "spherical"],
    "square": ["rectangular", "boxy"],
    "athletic": ["sport", "sports", "fitness", "exercise"],
}

BRAND_ALIASES: Dict[str, str] = {
    "nike air": "nike",
    "air jordan": "jordan",
    "jordan brand": "jordan",
    "adidas originals": "adidas",
    "three stripes": "adidas",
    "puma suede": "puma",
    "converse chuck": "converse",
    "chuck taylor": "converse",
    "vans old skool": "vans",
    "reebok classic": "reebok",
    "new balance 990": "new balance",
    "asics gel": "asics",
    "under armour curry": "under armour",
}


def extract_image_path(query: str) -> Optional[str]:
    path_patterns = [
        r"image\s+([^\s]+\.(jpg|jpeg|png|bmp|tiff))",
        r"file\s+([^\s]+\.(jpg|jpeg|png|bmp|tiff))",
        r"([^\s]+\.(jpg|jpeg|png|bmp|tiff))",
    ]
    for pattern in path_patterns:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def extract_similarity_threshold(query: str) -> float:
    if "very similar" in query or "exact match" in query:
        return 0.9
    if "similar" in query or "like" in query:
        return 0.7
    if "somewhat similar" in query or "related" in query:
        return 0.5
    return 0.7


def extract_limit(query: str) -> int:
    number_words = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "ten": 10, "twenty": 20, "fifty": 50, "hundred": 100,
    }
    for word, number in number_words.items():
        if word in query:
            return number
    number_match = re.search(r"(\d+)\s+(results?|items?|shoes?)", query)
    if number_match:
        return int(number_match.group(1))
    return 10


_MALICIOUS_PATTERNS = [
    r"<script.*?>", r"javascript:", r"on\w+\s*=", r"eval\s*\(", r"exec\s*\(",
]


def validate_query(query: str) -> Tuple[bool, str]:
    if not query or len(query.strip()) < 2:
        return False, "Query too short"
    if len(query) > 500:
        return False, "Query too long"
    for pattern in _MALICIOUS_PATTERNS:
        if re.search(pattern, query, re.IGNORECASE):
            return False, "Query contains potentially malicious content"
    return True, "Valid query"
