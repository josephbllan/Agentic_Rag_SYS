from abc import ABC
import logging


class BaseService(ABC):
    def __init__(self, service_name: str):
        self._service_name = service_name
        self._logger = logging.getLogger(self.__class__.__name__)
        self._is_initialized = False

    @property
    def service_name(self) -> str:
        return self._service_name

    @property
    def is_initialized(self) -> bool:
        return self._is_initialized

    def initialize(self) -> None:
        self._logger.info(f"Initializing {self._service_name} service...")
        self._is_initialized = True

    def shutdown(self) -> None:
        self._logger.info(f"Shutting down {self._service_name} service...")
        self._is_initialized = False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self._service_name}', initialized={self._is_initialized})"
