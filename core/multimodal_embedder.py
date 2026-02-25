"""Combined image and text embedding system."""
from typing import Dict
import numpy as np
from core.image_embedder import ImageEmbedder
from core.text_embedder import TextEmbedder


class MultiModalEmbedder:
    def __init__(self):
        self.image_embedder = ImageEmbedder("clip")
        self.text_embedder = TextEmbedder()
        self.clip_embedder = ImageEmbedder("clip")
        self._resnet_embedder = None

    @property
    def resnet_embedder(self):
        if self._resnet_embedder is None:
            self._resnet_embedder = ImageEmbedder("resnet")
        return self._resnet_embedder

    def encode_image(self, image_path: str) -> Dict[str, np.ndarray]:
        return {
            "clip": self.image_embedder.encode_image(image_path),
            "resnet": self.resnet_embedder.encode_image(image_path),
        }

    def encode_text(self, text: str) -> Dict[str, np.ndarray]:
        return {
            "clip": self.clip_embedder.encode_text(text),
            "sentence_transformer": self.text_embedder.encode_text(text),
        }

    def encode_image_text_pair(self, image_path: str, text: str) -> Dict[str, np.ndarray]:
        return {
            "image_clip": self.image_embedder.encode_image(image_path),
            "image_resnet": self.resnet_embedder.encode_image(image_path),
            "text_clip": self.clip_embedder.encode_text(text),
            "text_sentence_transformer": self.text_embedder.encode_text(text),
        }
