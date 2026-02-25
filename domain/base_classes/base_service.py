from abc import ABC
import logging


class BaseService(ABC):
    def __init__(self, service_name: str):
        """Initializes the service with the given name.
        Sets up logging and marks the service as not yet initialized.
        """
        self._service_name = service_name
        self._logger = logging.getLogger(self.__class__.__name__)
        self._is_initialized = False

    @property
    def service_name(self) -> str:
        """Returns the name of this service."""
        return self._service_name

    @property
    def is_initialized(self) -> bool:
        """Indicates whether the service has been initialized."""
        return self._is_initialized

    def initialize(self) -> None:
        """Initializes the service and marks it as ready for use."""
        self._logger.info(f"Initializing {self._service_name} service...")
        self._is_initialized = True

    def shutdown(self) -> None:
        """Shuts down the service and marks it as no longer initialized."""
        self._logger.info(f"Shutting down {self._service_name} service...")
        self._is_initialized = False

    def __repr__(self) -> str:
        """Returns a string representation including service name and initialization state."""
        return f"{self.__class__.__name__}(name='{self._service_name}', initialized={self._is_initialized})"
