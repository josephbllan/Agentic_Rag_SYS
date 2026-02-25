"""Embedding cache manager and utility functions."""
import numpy as np
from typing import List, Dict, Any
from pathlib import Path

from core.multimodal_embedder import MultiModalEmbedder
from core.utils import stable_text_hash


class EmbeddingManager:
    """Manage and cache embeddings."""

    def __init__(self, cache_dir: str = "embeddings_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.multimodal_embedder = MultiModalEmbedder()

    def get_image_embedding(
        self, image_path: str, model_type: str = "clip", use_cache: bool = True
    ) -> np.ndarray:
        if use_cache:
            cache_path = self.cache_dir / f"{Path(image_path).stem}_{model_type}.npy"
            if cache_path.exists():
                return np.load(cache_path)
        if model_type == "clip":
            embedding = self.multimodal_embedder.image_embedder.encode_image(image_path)
        elif model_type == "resnet":
            embedding = self.multimodal_embedder.resnet_embedder.encode_image(image_path)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
        if use_cache:
            np.save(cache_path, embedding)
        return embedding

    def get_text_embedding(
        self, text: str, model_type: str = "sentence_transformer",
        use_cache: bool = True,
    ) -> np.ndarray:
        if use_cache:
            cache_key = f"{stable_text_hash(text)}_{model_type}"
            cache_path = self.cache_dir / f"text_{cache_key}.npy"
            if cache_path.exists():
                return np.load(cache_path)
        if model_type == "clip":
            embedding = self.multimodal_embedder.clip_embedder.encode_text(text)
        elif model_type == "sentence_transformer":
            embedding = self.multimodal_embedder.text_embedder.encode_text(text)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
        if use_cache:
            np.save(cache_path, embedding)
        return embedding

    def batch_process_images(
        self, image_paths: List[str], model_type: str = "clip"
    ) -> List[np.ndarray]:
        if model_type == "clip":
            embedder = self.multimodal_embedder.image_embedder
        elif model_type == "resnet":
            embedder = self.multimodal_embedder.resnet_embedder
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
        return embedder.encode_images_batch(image_paths)

    def batch_process_texts(
        self, texts: List[str], model_type: str = "sentence_transformer"
    ) -> List[np.ndarray]:
        if model_type == "clip":
            embedder = self.multimodal_embedder.clip_embedder
        elif model_type == "sentence_transformer":
            embedder = self.multimodal_embedder.text_embedder
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
        return embedder.encode_texts_batch(texts)

    def clear_cache(self):
        import shutil
        if self.cache_dir.exists():
            shutil.rmtree(self.cache_dir)
        self.cache_dir.mkdir(exist_ok=True)


def normalize_embedding(embedding: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(embedding)
    return embedding / norm if norm > 0 else embedding


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(normalize_embedding(a), normalize_embedding(b)))


def euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b))


def create_embedding_from_metadata(metadata: Dict[str, Any]) -> np.ndarray:
    features: List[int] = []
    for cat, vals in [
        ("pattern", ["zigzag", "circular", "square", "diamond", "brand_logo", "other"]),
        ("shape", ["round", "square", "oval", "irregular", "elongated"]),
        ("size", ["small", "medium", "large", "extra_large"]),
        ("brand", [
            "nike", "adidas", "puma", "converse", "vans", "reebok",
            "new_balance", "asics", "under_armour", "jordan", "other",
        ]),
    ]:
        features.extend(1 if metadata.get(cat) == v else 0 for v in vals)
    return np.array(features, dtype=np.float32)
