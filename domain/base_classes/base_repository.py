from abc import ABC, abstractmethod
from typing import Generic, List, Dict, Any, Optional
import logging
from ..types import T


class BaseRepository(ABC, Generic[T]):
    def __init__(self, entity_type: type):
        self._entity_type = entity_type
        self._logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def add(self, entity: T) -> T:
        pass

    @abstractmethod
    def get_by_id(self, id: Any) -> Optional[T]:
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        pass

    @abstractmethod
    def delete(self, id: Any) -> bool:
        pass

    @abstractmethod
    def find(self, criteria: Dict[str, Any]) -> List[T]:
        pass

    def count(self) -> int:
        return len(self.find({}))

    def exists(self, id: Any) -> bool:
        return self.get_by_id(id) is not None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(entity_type={self._entity_type.__name__})"
