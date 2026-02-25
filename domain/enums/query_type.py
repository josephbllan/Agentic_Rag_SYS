from enum import Enum

class QueryType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    HYBRID = "hybrid"
    SEMANTIC = "semantic"
    METADATA = "metadata"
    NATURAL_LANGUAGE = "natural_language"
