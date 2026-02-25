"""Text embedding generation using Sentence Transformers."""
import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer
from config.settings import MODEL_CONFIG
import logging

logger = logging.getLogger(__name__)


class TextEmbedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initializes the text embedder with the specified sentence-transformer
        model and loads it onto the configured device."""
        self.model_name = model_name
        self.device = MODEL_CONFIG["sentence_transformer"]["device"]
        self._load_model()

    def _load_model(self):
        """Loads the sentence-transformer model and determines its
        output embedding dimension."""
        self.model = SentenceTransformer(self.model_name, device=self.device)
        self.dimension = self.model.get_sentence_embedding_dimension()
        logger.info(f"Sentence Transformer model loaded: {self.model_name}")

    def encode_text(self, text: str) -> np.ndarray:
        """Encodes a single text string into an embedding vector, returning
        a zero vector on failure."""
        try:
            embedding = self.model.encode([text])
            return embedding[0]
        except Exception as e:
            logger.error(f"Failed to encode text '{text}': {e}")
            return np.zeros(self.dimension)

    def encode_texts_batch(self, texts: List[str], batch_size: int = 32) -> List[np.ndarray]:
        """Encodes a list of text strings in batch and returns their
        embedding vectors, using zero vectors as fallback on error."""
        try:
            embeddings = self.model.encode(texts, batch_size=batch_size)
            return [emb for emb in embeddings]
        except Exception as e:
            logger.error(f"Failed to encode texts batch: {e}")
            return [np.zeros(self.dimension) for _ in texts]
