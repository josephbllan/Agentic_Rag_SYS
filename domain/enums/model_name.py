from enum import Enum

class ModelName(str, Enum):
    CLIP_VIT_B32 = "ViT-B/32"
    CLIP_VIT_L14 = "ViT-L/14"
    RESNET50 = "resnet50"
    RESNET101 = "resnet101"
    SENTENCE_MINI_LM = "all-MiniLM-L6-v2"
