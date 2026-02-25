"""RAGSystem -- main orchestrator for image search and analysis."""
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

from core.search_engine import create_search_engine
from core.embeddings import EmbeddingManager
from core.query_processor import QueryProcessor
from config.database import create_tables, test_connection
from config.settings import DATA_DIR, VECTOR_DB_DIR, IMAGE_CONFIG

logger = logging.getLogger(__name__)


class RAGSystem:
    """Main RAG System orchestrator."""

    def __init__(self, vector_backend: str = "faiss"):
        """Initializes the RAG system with the specified vector backend
        and triggers full system setup.
        """
        self.vector_backend = vector_backend
        self.search_engine = None
        self.embedding_manager = None
        self.query_processor = None
        self._initialize_system()

    def _initialize_system(self):
        """Connects to the database, creates tables, and instantiates
        the search engine, embedding manager, and query processor.
        """
        logger.info("Initializing RAG System...")
        if not test_connection():
            raise RuntimeError("Database connection failed")
        create_tables()
        self.search_engine = create_search_engine(self.vector_backend)
        self.embedding_manager = EmbeddingManager()
        self.query_processor = QueryProcessor()
        logger.info("RAG System initialized successfully!")

    def index_images(self, image_directory: Optional[str] = None, batch_size: int = 32) -> Dict[str, Any]:
        """Discovers image files in the given directory and indexes them
        into the vector database in batches, returning a summary dict.
        """
        try:
            image_directory = image_directory or str(DATA_DIR)
            image_paths = self._find_image_files(image_directory)
            if not image_paths:
                return {"status": "no_images", "count": 0}

            indexed = failed = 0
            for i in range(0, len(image_paths), batch_size):
                for path in image_paths[i : i + batch_size]:
                    try:
                        emb = self.embedding_manager.get_image_embedding(path, "clip")
                        meta = self._extract_metadata_from_path(path)
                        self.search_engine.vector_db.add_vectors(
                            vectors=emb.reshape(1, -1), metadata=[meta], ids=[f"img_{indexed}"]
                        )
                        indexed += 1
                    except Exception as e:
                        logger.error(f"Failed to index {path}: {e}")
                        failed += 1
            return {"status": "completed", "indexed_count": indexed, "failed_count": failed, "total_found": len(image_paths)}
        except Exception as e:
            logger.error(f"Image indexing failed: {e}")
            return {"status": "failed", "error": str(e)}

    def search(self, query: str, search_type: str = "text", **kwargs) -> List[Dict[str, Any]]:
        """Dispatches a search request to the appropriate engine method
        based on the specified search type (text, image, hybrid, semantic, or natural).
        """
        try:
            dispatch = {
                "text": lambda: self.search_engine.text_to_image_search(query, **kwargs),
                "image": lambda: self.search_engine.image_to_image_search(query, **kwargs),
                "hybrid": lambda: self.search_engine.hybrid_search(query=query, **kwargs),
                "semantic": lambda: self.search_engine.semantic_search(query, **kwargs),
            }
            if search_type == "natural":
                intent = self.query_processor.process_query(query)
                return self.search_engine.hybrid_search(
                    query=" ".join(intent.search_terms), filters=intent.filters, limit=intent.limit
                )
            fn = dispatch.get(search_type)
            if fn is None:
                raise ValueError(f"Unsupported search type: {search_type}")
            return fn()
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    def get_recommendations(self, image_path: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Returns visually similar image recommendations for the
        given image path, delegating to the search engine.
        """
        try:
            return self.search_engine.get_recommendations(image_path, limit)
        except Exception as e:
            logger.error(f"Recommendations failed: {e}")
            return []

    def get_stats(self) -> Dict[str, Any]:
        """Aggregates and returns statistics from the search engine,
        vector database, and system configuration.
        """
        try:
            return {
                "search_engine": self.search_engine.get_search_stats(),
                "vector_db": self.search_engine.vector_db.get_stats(),
                "system": {"vector_backend": self.vector_backend, "data_directory": str(DATA_DIR), "vector_db_directory": str(VECTOR_DB_DIR)},
            }
        except Exception as e:
            logger.error(f"Stats retrieval failed: {e}")
            return {"error": str(e)}

    def _find_image_files(self, directory: str) -> List[str]:
        """Recursively scans the directory for supported image formats
        and returns a sorted list of file paths.
        """
        d = Path(directory)
        if not d.exists():
            return []
        paths: List[str] = []
        for ext in IMAGE_CONFIG["supported_formats"]:
            paths.extend(str(p) for p in d.glob(f"**/*{ext}"))
        return sorted(paths)

    def _extract_metadata_from_path(self, image_path: str) -> Dict[str, Any]:
        """Parses the image filename to extract structured metadata
        such as pattern, shape, size, and brand.
        """
        p = Path(image_path)
        parts = p.stem.split("_")
        meta: Dict[str, Any] = {"filename": p.name, "original_path": str(image_path), "pattern": "other", "shape": "other", "size": "medium", "brand": "other"}
        if len(parts) >= 6:
            valid_patterns = {"zigzag", "circular", "square", "diamond", "brand_logo", "other"}
            valid_shapes = {"round", "square", "oval", "irregular", "elongated"}
            valid_sizes = {"small", "medium", "large", "extra_large"}
            valid_brands = {"nike", "adidas", "puma", "converse", "vans", "reebok", "new_balance", "asics", "under_armour", "jordan", "other"}
            meta["pattern"] = parts[2] if parts[2] in valid_patterns else "other"
            meta["shape"] = parts[3] if parts[3] in valid_shapes else "other"
            meta["size"] = parts[4] if parts[4] in valid_sizes else "medium"
            meta["brand"] = parts[5] if parts[5] in valid_brands else "other"
        return meta
