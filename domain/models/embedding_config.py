from pydantic import BaseModel, Field, validator
from ..enums import ModelName


class EmbeddingConfig(BaseModel):
    model_name: ModelName
    device: str = "cpu"
    batch_size: int = Field(32, gt=0, le=128)
    dimension: int = Field(512, gt=0)
    cache_enabled: bool = True

    @validator('device')
    def validate_device(cls, v: str) -> str:
        if v not in ['cpu', 'cuda', 'mps']:
            raise ValueError('Device must be cpu, cuda, or mps')
        return v

    class Config:
        use_enum_values = True
