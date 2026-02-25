from pydantic import BaseModel, Field
from ..enums import VectorBackend


class VectorDatabaseConfig(BaseModel):
    backend: VectorBackend
    collection_name: str = "shoe_images"
    dimension: int = Field(512, gt=0)
    index_type: str = "IVFFlat"
    nlist: int = Field(1000, gt=0)
    nprobe: int = Field(10, gt=0)
    distance_metric: str = "cosine"

    class Config:
        use_enum_values = True
