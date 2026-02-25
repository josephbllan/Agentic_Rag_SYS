from typing import Protocol, List, Any, Optional, runtime_checkable
from ..models import SearchQuery, SearchResultItem


@runtime_checkable
class ISearchService(Protocol):
    def search(self, query: SearchQuery) -> List[SearchResultItem]:
        """Performs a search using the given structured search query."""
        ...

    def search_text(self, query_text: str, **kwargs: Any) -> List[SearchResultItem]:
        """Performs a text-based search using the provided query string."""
        ...

    def search_image(self, image_path: str, **kwargs: Any) -> List[SearchResultItem]:
        """Performs an image-based search using the image at the given path."""
        ...

    def search_hybrid(self, query_text: Optional[str] = None, image_path: Optional[str] = None, **kwargs: Any) -> List[SearchResultItem]:
        """Performs a hybrid search combining text and image inputs."""
        ...
