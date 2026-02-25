"""Vector Database Management -- re-exports + factory function."""
import numpy as np
from config.settings import MODEL_CONFIG

from core.vector_db_base import BaseVectorDB
from core.faiss_db import FAISSVectorDB
from core.chroma_db import ChromaVectorDB

VectorDatabase = BaseVectorDB


def create_vector_db(
    backend: str = "faiss", collection_name: str = "shoe_images"
) -> BaseVectorDB:
    dim = MODEL_CONFIG["clip"].get("dimension", 512)
    if backend == "faiss":
        return FAISSVectorDB(dimension=dim, collection_name=collection_name)
    if backend == "chroma":
        return ChromaVectorDB(dimension=dim, collection_name=collection_name)
    raise ValueError(f"Unsupported backend: {backend}")


def get_embedding_dimension(model_name: str) -> int:
    dimensions = {
        "ViT-B/32": 512, "ViT-L/14": 768,
        "resnet50": 2048, "all-MiniLM-L6-v2": 384,
    }
    return dimensions.get(model_name, 512)


def validate_vector(vector: np.ndarray, expected_dim: int) -> bool:
    return vector.shape[-1] == expected_dim


__all__ = [
    "BaseVectorDB", "FAISSVectorDB", "ChromaVectorDB",
    "VectorDatabase", "create_vector_db",
    "get_embedding_dimension", "validate_vector",
]
