from enum import Enum

class PatternType(str, Enum):
    ZIGZAG = "zigzag"
    CIRCULAR = "circular"
    SQUARE = "square"
    DIAMOND = "diamond"
    BRAND_LOGO = "brand_logo"
    OTHER = "other"
