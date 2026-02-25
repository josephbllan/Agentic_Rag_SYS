from typing import Protocol, List, runtime_checkable
from ..models import ImageMetadata


@runtime_checkable
class IMetadataExtractor(Protocol):
    def extract(self, file_path: str) -> ImageMetadata: ...
    def extract_batch(self, file_paths: List[str]) -> List[ImageMetadata]: ...
