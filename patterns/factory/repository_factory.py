from typing import Dict, Any, Type
import logging


class RepositoryFactory:
    _repository_classes: Dict[str, Type] = {}
    _logger = logging.getLogger("RepositoryFactory")

    @classmethod
    def register_repository(cls, entity_type: str, repository_class: Type) -> None:
        """Registers a repository class under the given entity type identifier."""
        cls._repository_classes[entity_type] = repository_class

    @classmethod
    def create_repository(cls, entity_type: str, **kwargs) -> Any:
        """Creates and returns a repository instance for the specified entity type.
        Raises ValueError if the entity type has not been registered.
        """
        if entity_type not in cls._repository_classes:
            raise ValueError(f"Unknown entity: {entity_type}")
        return cls._repository_classes[entity_type](**kwargs)

    @classmethod
    def get_supported_types(cls) -> list[str]:
        """Returns a list of all registered entity type identifiers."""
        return list(cls._repository_classes.keys())
