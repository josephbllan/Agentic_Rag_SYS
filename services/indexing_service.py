"""Indexing Service -- batch processing and metadata extraction."""
from typing import List, Dict, Any, Optional
from pathlib import Path
import time

from .base_service import BaseService
from ..domain.models import IndexingResult, ImageMetadata
from ..domain.interfaces import IVectorDatabase, IEmbeddingModel
from ..patterns.observer import EventPublisher


class IndexingService(BaseService):
    """Service for indexing images and extracting embeddings."""

    def __init__(
        self,
        embedding_model: Optional[IEmbeddingModel] = None,
        vector_db: Optional[IVectorDatabase] = None,
        event_publisher: Optional[EventPublisher] = None,
    ):
        """Initializes the indexing service with optional embedding model,
        vector database, and event publisher dependencies.
        """
        super().__init__("IndexingService")
        self._embedding_model = embedding_model
        self._vector_db = vector_db
        self._event_publisher = event_publisher
        self._total_indexed = 0
        self._total_failed = 0

    def index_directory(
        self, directory_path: str, batch_size: int = 32, recursive: bool = True
    ) -> IndexingResult:
        """Scans the given directory for images and indexes them in batches,
        publishing progress events and returning an IndexingResult summary.
        """
        self._ensure_initialized()
        dir_path = Path(directory_path)
        if not dir_path.exists():
            raise ValueError(f"Directory does not exist: {directory_path}")

        start_time = time.time()
        image_files = self._find_images(dir_path, recursive)
        total_files = len(image_files)
        if total_files == 0:
            return IndexingResult(total_processed=0, successful=0, failed=0, execution_time=0.0)

        successful = failed = 0
        errors: List[str] = []
        for i in range(0, total_files, batch_size):
            batch = image_files[i : i + batch_size]
            for image_path in batch:
                try:
                    self._index_single_image(image_path)
                    successful += 1
                    if self._event_publisher:
                        self._event_publisher.publish("image_indexed", {"filename": image_path.name, "path": str(image_path)})
                except Exception as e:
                    failed += 1
                    errors.append(f"{image_path.name}: {e}")
                    self._logger.warning(f"Failed to index {image_path.name}: {e}")
                    if self._event_publisher:
                        self._event_publisher.publish("indexing_failed", {"filename": image_path.name, "error": str(e)})

        elapsed = time.time() - start_time
        self._total_indexed += successful
        self._total_failed += failed
        self._record_metric("total_indexed", self._total_indexed)
        self._record_metric("total_failed", self._total_failed)

        if self._event_publisher:
            self._event_publisher.publish("indexing_complete", {
                "total": total_files, "successful": successful, "failed": failed, "execution_time": elapsed,
            })

        return IndexingResult(
            total_processed=total_files, successful=successful,
            failed=failed, execution_time=elapsed, errors=errors[:10],
        )

    def _index_single_image(self, image_path: Path) -> None:
        """Generates an embedding for a single image and stores it
        along with extracted metadata in the vector database.
        """
        if not self._embedding_model or not self._vector_db:
            raise RuntimeError("Embedding model and vector DB required")
        embedding = self._embedding_model.encode(str(image_path))
        metadata = self._extract_metadata(image_path)
        self._vector_db.add_vectors(
            vectors=embedding.reshape(1, -1), metadata=[metadata.dict()], ids=[f"img_{image_path.stem}"]
        )

    def _find_images(self, directory: Path, recursive: bool) -> List[Path]:
        """Collects image file paths from the directory, optionally
        searching recursively, and returns them sorted.
        """
        exts = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}
        files: List[Path] = []
        for ext in exts:
            files.extend(directory.rglob(f"*{ext}") if recursive else directory.glob(f"*{ext}"))
        return sorted(files)

    def _extract_metadata(self, image_path: Path) -> ImageMetadata:
        """Creates an ImageMetadata instance from the given image path."""
        return ImageMetadata(filename=image_path.name, original_path=str(image_path))

    def get_statistics(self) -> Dict[str, Any]:
        """Computes and returns indexing statistics including totals,
        success rate, and current service status.
        """
        total = self._total_indexed + self._total_failed
        return {
            "total_indexed": self._total_indexed,
            "total_failed": self._total_failed,
            "success_rate": self._total_indexed / total if total > 0 else 0.0,
            "service_status": "active" if self._is_initialized else "inactive",
        }
