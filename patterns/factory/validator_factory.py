from typing import Dict, Any, Type
import logging


class ValidatorFactory:
    _validator_classes: Dict[str, Type] = {}
    _logger = logging.getLogger("ValidatorFactory")

    @classmethod
    def register_validator(cls, validator_type: str, validator_class: Type) -> None:
        """Registers a validator class under the given validator type identifier."""
        cls._validator_classes[validator_type] = validator_class

    @classmethod
    def create_validator(cls, validator_type: str, **kwargs) -> Any:
        """Creates and returns a validator instance of the specified type.
        Raises ValueError if the validator type has not been registered.
        """
        if validator_type not in cls._validator_classes:
            raise ValueError(f"Unknown validator: {validator_type}")
        return cls._validator_classes[validator_type](**kwargs)

    @classmethod
    def get_supported_types(cls) -> list[str]:
        """Returns a list of all registered validator type identifiers."""
        return list(cls._validator_classes.keys())
