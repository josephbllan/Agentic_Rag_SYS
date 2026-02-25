from enum import Enum

class ShapeType(str, Enum):
    ROUND = "round"
    SQUARE = "square"
    OVAL = "oval"
    IRREGULAR = "irregular"
    ELONGATED = "elongated"
