from typing import Dict, Any, Type, Optional
import logging


class ServiceFactory:
    _service_classes: Dict[str, Type] = {}
    _service_instances: Dict[str, Any] = {}
    _logger = logging.getLogger("ServiceFactory")

    @classmethod
    def register_service(cls, service_name: str, service_class: Type) -> None:
        """Registers a service class under the given service name identifier."""
        cls._service_classes[service_name] = service_class

    @classmethod
    def create_service(cls, service_name: str, cached: bool = True, **kwargs) -> Any:
        """Creates and returns a service instance, optionally caching it for reuse.
        Returns the cached instance if one exists and caching is enabled.
        """
        if cached and service_name in cls._service_instances:
            return cls._service_instances[service_name]
        if service_name not in cls._service_classes:
            raise ValueError(f"Unknown service: {service_name}")
        service = cls._service_classes[service_name](**kwargs)
        if cached:
            cls._service_instances[service_name] = service
        return service

    @classmethod
    def get_service(cls, service_name: str) -> Optional[Any]:
        """Retrieves a previously cached service instance by name, or None if not found."""
        return cls._service_instances.get(service_name)

    @classmethod
    def clear_cache(cls) -> None:
        """Clears all cached service instances from the factory."""
        cls._service_instances.clear()
