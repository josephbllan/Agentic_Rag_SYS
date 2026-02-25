from enum import Enum

class VectorBackend(str, Enum):
    FAISS = "faiss"
    CHROMA = "chroma"
