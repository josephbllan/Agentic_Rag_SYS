"""Combined image and text embedding system."""
from typing import Dict
import numpy as np
from core.image_embedder import ImageEmbedder
from core.text_embedder import TextEmbedder


class MultiModalEmbedder:
    def __init__(self):
        """Initializes CLIP and sentence-transformer embedders eagerly,
        deferring the ResNet embedder until first use."""
        self.image_embedder = ImageEmbedder("clip")
        self.text_embedder = TextEmbedder()
        self.clip_embedder = ImageEmbedder("clip")
        self._resnet_embedder = None

    @property
    def resnet_embedder(self):
        """Lazily initializes and returns the ResNet image embedder
        on first access."""
        if self._resnet_embedder is None:
            self._resnet_embedder = ImageEmbedder("resnet")
        return self._resnet_embedder

    def encode_image(self, image_path: str) -> Dict[str, np.ndarray]:
        """Encodes an image using both CLIP and ResNet models and returns
        a dictionary keyed by model name."""
        return {
            "clip": self.image_embedder.encode_image(image_path),
            "resnet": self.resnet_embedder.encode_image(image_path),
        }

    def encode_text(self, text: str) -> Dict[str, np.ndarray]:
        """Encodes text using both CLIP and sentence-transformer models
        and returns a dictionary keyed by model name."""
        return {
            "clip": self.clip_embedder.encode_text(text),
            "sentence_transformer": self.text_embedder.encode_text(text),
        }

    def encode_image_text_pair(self, image_path: str, text: str) -> Dict[str, np.ndarray]:
        """Encodes an image-text pair across all available models and returns
        a dictionary with embeddings keyed by modality and model."""
        return {
            "image_clip": self.image_embedder.encode_image(image_path),
            "image_resnet": self.resnet_embedder.encode_image(image_path),
            "text_clip": self.clip_embedder.encode_text(text),
            "text_sentence_transformer": self.text_embedder.encode_text(text),
        }
