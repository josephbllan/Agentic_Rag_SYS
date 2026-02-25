from typing import Protocol, List, runtime_checkable
from ..models import ImageMetadata


@runtime_checkable
class IMetadataExtractor(Protocol):
    def extract(self, file_path: str) -> ImageMetadata:
        """Extracts metadata from the image file at the given path."""
        ...

    def extract_batch(self, file_paths: List[str]) -> List[ImageMetadata]:
        """Extracts metadata from multiple image files and returns a list of results."""
        ...
