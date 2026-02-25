"""Image embedding generation using CLIP or ResNet."""
import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
from typing import List
import clip
import torchvision.models as models
from config.settings import MODEL_CONFIG
import logging

logger = logging.getLogger(__name__)


class ImageEmbedder:
    """Generate embeddings for images using CLIP or ResNet."""

    def __init__(self, model_type: str = "clip"):
        self.model_type = model_type
        self.device = torch.device(MODEL_CONFIG["clip"]["device"])
        self._load_model()

    def _load_model(self):
        if self.model_type == "clip":
            self._load_clip()
        elif self.model_type == "resnet":
            self._load_resnet()
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")

    def _load_clip(self):
        model_name = MODEL_CONFIG["clip"]["model_name"]
        self.model, self.preprocess = clip.load(model_name, device=self.device)
        self.model.eval()
        self.dimension = 512 if "ViT-B" in model_name else 768
        logger.info(f"CLIP model loaded: {model_name}")

    def _load_resnet(self):
        model_name = MODEL_CONFIG["resnet"]["model_name"]
        self.model = models.__dict__[model_name](
            pretrained=MODEL_CONFIG["resnet"]["pretrained"]
        )
        self.model = self.model.to(self.device)
        self.model.eval()
        self.dimension = 2048
        self.preprocess = transforms.Compose([
            transforms.Resize(256), transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
            ),
        ])
        logger.info(f"ResNet model loaded: {model_name}")

    def encode_image(self, image_path: str) -> np.ndarray:
        try:
            image = Image.open(image_path).convert("RGB")
            image = self.preprocess(image).unsqueeze(0).to(self.device)
            with torch.no_grad():
                if self.model_type == "clip":
                    feat = self.model.encode_image(image)
                    feat = feat / feat.norm(dim=-1, keepdim=True)
                else:
                    feat = self.model(image)
                    feat = torch.nn.functional.adaptive_avg_pool2d(feat, (1, 1))
                    feat = feat.view(feat.size(0), -1)
            return feat.cpu().numpy().flatten()
        except Exception as e:
            logger.error(f"Failed to encode image {image_path}: {e}")
            return np.zeros(self.dimension)

    def encode_images_batch(
        self, image_paths: List[str], batch_size: int = 32
    ) -> List[np.ndarray]:
        embeddings = []
        for i in range(0, len(image_paths), batch_size):
            for path in image_paths[i : i + batch_size]:
                embeddings.append(self.encode_image(path))
        return embeddings

    def encode_text(self, text: str) -> np.ndarray:
        if self.model_type != "clip":
            raise ValueError("Text encoding only available for CLIP model")
        try:
            tokens = clip.tokenize([text]).to(self.device)
            with torch.no_grad():
                feat = self.model.encode_text(tokens)
                feat = feat / feat.norm(dim=-1, keepdim=True)
            return feat.cpu().numpy().flatten()
        except Exception as e:
            logger.error(f"Failed to encode text '{text}': {e}")
            return np.zeros(self.dimension)
