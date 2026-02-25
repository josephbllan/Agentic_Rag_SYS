"""Embeddings -- re-exports for backward compatibility."""
from core.image_embedder import ImageEmbedder
from core.text_embedder import TextEmbedder
from core.multimodal_embedder import MultiModalEmbedder
from core.embedding_manager import (
    EmbeddingManager,
    normalize_embedding,
    cosine_similarity,
    euclidean_distance,
    create_embedding_from_metadata,
)

__all__ = [
    "ImageEmbedder",
    "TextEmbedder",
    "MultiModalEmbedder",
    "EmbeddingManager",
    "normalize_embedding",
    "cosine_similarity",
    "euclidean_distance",
    "create_embedding_from_metadata",
]
